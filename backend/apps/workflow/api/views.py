from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db import transaction
from apps.requests.models import Request
from .serializers import InboxRequestSerializer, ExecuteTransitionSerializer
from apps.workflow.services import can_user_execute_transition
from ..models import ActionLog

class InboxAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        queryset = Request.objects.filter(
            current_state__isnull=False,
            current_state__is_final=False
        ).select_related(
            'current_state', 'user', 'form_version__form_definition'
        ).prefetch_related(
            'current_state__out_transitions'
        ).order_by('-created_at')
        
        inbox_requests = [req for req in queryset if any(
            can_user_execute_transition(req, t, user) for t in req.current_state.out_transitions.all()
        )]
        serializer = InboxRequestSerializer(inbox_requests, many=True, context={'request': request})
        return Response(serializer.data)

class ExecuteTransitionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ExecuteTransitionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.validated_data
            req, trans = data['request_obj'], data['transition_obj']
            with transaction.atomic():
                ActionLog.objects.create(
                    request=req, user=request.user, transition=trans,
                    from_state=req.current_state, to_state=trans.to_state,
                    comment=data.get('comment', '')
                )
                req.current_state = trans.to_state
                req.save()
            return Response({'detail': 'Success', 'new_state': trans.to_state.name})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
