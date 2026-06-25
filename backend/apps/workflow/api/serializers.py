from rest_framework import serializers
from apps.requests.models import Request
from apps.workflow.models import State, Transition

class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = ['id', 'name', 'to_state']

class InboxRequestSerializer(serializers.ModelSerializer):
    current_state_name = serializers.ReadOnlyField(source='current_state.name')
    creator_name = serializers.ReadOnlyField(source='user.get_full_name')
    form_name = serializers.ReadOnlyField(source='form_version.form_definition.name')
    available_actions = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['id', 'title', 'current_state_name', 'creator_name', 'form_name', 'created_at', 'available_actions']

    def get_available_actions(self, obj):
        from apps.workflow.services import can_user_execute_transition
        user = self.context['request'].user
        transitions = obj.current_state.out_transitions.all()
        valid_transitions = [t for t in transitions if can_user_execute_transition(obj, t, user)]
        return TransitionSerializer(valid_transitions, many=True).data

class ExecuteTransitionSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    transition_id = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        from apps.workflow.services import can_user_execute_transition
        try:
            req = Request.objects.get(id=data['request_id'])
        except Request.DoesNotExist:
            raise serializers.ValidationError('Request not found.')
        try:
            trans = Transition.objects.get(id=data['transition_id'])
        except Transition.DoesNotExist:
            raise serializers.ValidationError('Transition not found.')
        if req.current_state != trans.from_state:
            raise serializers.ValidationError('عملیات در وضعیت فعلی مجاز نیست.')
        user = self.context['request'].user
        if not can_user_execute_transition(req, trans, user):
            raise serializers.ValidationError('عدم دسترسی برای این عملیات.')
        data['request_obj'] = req
        data['transition_obj'] = trans
        return data
