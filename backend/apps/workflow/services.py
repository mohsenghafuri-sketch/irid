from django.core.exceptions import ValidationError
from django.db import transaction

from apps.organization.models import UserAssignment
from apps.requests.models import RequestHistory
from apps.workflow.models import Transition


def get_initial_state(workflow):
    state = workflow.states.filter(is_initial=True).first()
    if not state:
        raise ValidationError("No initial state is defined for this workflow.")
    return state


def resolve_transition_assignee(request_obj, transition):
    assignment_type = transition.assignment_type
    assignment_data = transition.assignment_data

    if assignment_type == 'DIRECT_MANAGER':
        current_assignment = UserAssignment.objects.filter(
            user=request_obj.user,
            is_active=True
        ).select_related(
            'job_title__reports_to'
        ).first()

        if not current_assignment:
            return None

        return current_assignment.get_direct_superior_assignment()

    if assignment_type == 'SPECIFIC_USER':
        if not assignment_data:
            return None

        return UserAssignment.objects.filter(
            user_id=assignment_data,
            is_active=True
        ).first()

    if assignment_type == 'CREATOR':
        return UserAssignment.objects.filter(
            user=request_obj.user,
            is_active=True
        ).first()

    if assignment_type == 'ROLE':
        if not assignment_data:
            return None

        return UserAssignment.objects.filter(
            job_title__position__title=assignment_data,
            is_active=True
        ).first()

    return None


def get_available_transitions(request_obj):
    if not request_obj.current_state:
        return Transition.objects.none()

    return Transition.objects.filter(
        workflow=request_obj.current_state.workflow,
        from_state=request_obj.current_state
    ).select_related('from_state', 'to_state', 'workflow')


@transaction.atomic
def start_request(request_obj, workflow):
    if request_obj.current_state_id:
        raise ValidationError("Request already has a current state.")

    initial_state = get_initial_state(workflow)
    request_obj.current_state = initial_state
    request_obj.save(update_fields=['current_state', 'updated_at'])

    RequestHistory.objects.create(
        request=request_obj,
        from_state=None,
        to_state=initial_state,
        performed_by=request_obj.user,
        action_name='start_request',
        comment='Request started'
    )

    return request_obj


@transaction.atomic
def execute_transition(request_obj, transition, performed_by, comment=""):
    if request_obj.current_state_id != transition.from_state_id:
        raise ValidationError("Transition is not valid for the current request state.")

    request_obj.current_state = transition.to_state
    request_obj.save(update_fields=['current_state', 'updated_at'])

    RequestHistory.objects.create(
        request=request_obj,
        from_state=transition.from_state,
        to_state=transition.to_state,
        performed_by=performed_by,
        action_name=transition.name,
        comment=comment or ''
    )

    next_assignee = resolve_transition_assignee(request_obj, transition)

    return {
        "request": request_obj,
        "next_assignee": next_assignee,
        "to_state": transition.to_state,
    }
