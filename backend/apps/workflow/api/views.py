from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.requests.models import Request
from .serializers import InboxRequestSerializer
from apps.workflow.services import can_user_execute_transition

class InboxAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = Request.objects.filter(
            current_state__isnull=False,
            current_state__is_final=False
        ).select_related(
            'current_state', 
            'user', 
            'form_version__form_definition'
        ).prefetch_related(
            'current_state__out_transitions'
        ).order_by('-created_at')

        inbox_requests = []
        for req in queryset:
            transitions = req.current_state.out_transitions.all()
            is_assignee = any(can_user_execute_transition(req, t, user) for t in transitions)
            if is_assignee:
                inbox_requests.append(req)

        serializer = InboxRequestSerializer(
            inbox_requests, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
