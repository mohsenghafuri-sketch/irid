from rest_framework import serializers
from apps.workflow.models import State, Transition
from apps.requests.models import Request
from apps.workflow.services import get_available_transitions, can_user_execute_transition

class StateBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'code']

class InboxRequestSerializer(serializers.ModelSerializer):
    current_state = StateBriefSerializer(read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    form_name = serializers.CharField(source='form_version.form_definition.name', read_only=True)
    available_actions = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = [
            'id', 'tracking_code', 'user_full_name', 'form_name',
            'current_state', 'created_at', 'available_actions'
        ]

    def get_available_actions(self, obj):
        user = self.context.get('request').user
        transitions = get_available_transitions(obj)
        allowed = []
        for t in transitions:
            if can_user_execute_transition(obj, t, user):
                allowed.append({
                    "id": t.id,
                    "name": t.name,
                    "to_state": t.to_state.name
                })
        return allowed
