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


def get_user_primary_assignment(user):
    return UserAssignment.objects.filter(
        user=user,
        is_primary=True
    ).select_related(
        'job_title',
        'job_title__superior',
        'job_title__position',
        'job_title__department',
    ).first()


def get_direct_manager_assignment(user):
    current_assignment = get_user_primary_assignment(user)

    if not current_assignment:
        return None

    if not current_assignment.job_title_id:
        return None

    if not current_assignment.job_title.superior_id:
        return None

    return UserAssignment.objects.filter(
        job_title=current_assignment.job_title.superior,
        is_primary=True
    ).select_related(
        'user',
        'job_title',
        'job_title__position',
        'job_title__department',
    ).first()


def resolve_transition_assignee(request_obj, transition):
    assignment_type = transition.assignment_type
    assignment_data = transition.assignment_data

    if assignment_type == 'DIRECT_MANAGER':
        return get_direct_manager_assignment(request_obj.user)

    if assignment_type == 'SPECIFIC_USER':
        if not assignment_data:
            return None

        return UserAssignment.objects.filter(
            user_id=assignment_data,
            is_primary=True
        ).select_related(
            'user',
            'job_title',
            'job_title__position',
            'job_title__department',
        ).first()

    if assignment_type == 'CREATOR':
        return get_user_primary_assignment(request_obj.user)

    if assignment_type == 'ROLE':
        if not assignment_data:
            return None

        return UserAssignment.objects.filter(
            job_title__position__title=assignment_data,
            is_primary=True
        ).select_related(
            'user',
            'job_title',
            'job_title__position',
            'job_title__department',
        ).first()

    return None


def can_user_execute_transition(request_obj, transition, user):
    assignment_type = transition.assignment_type
    assignment_data = transition.assignment_data

    if assignment_type == 'CREATOR':
        return request_obj.user_id == user.id

    if assignment_type == 'SPECIFIC_USER':
        return str(user.id) == str(assignment_data)

    if assignment_type == 'DIRECT_MANAGER':
        manager_assignment = get_direct_manager_assignment(request_obj.user)
        return bool(manager_assignment and manager_assignment.user_id == user.id)

    if assignment_type == 'ROLE':
        return UserAssignment.objects.filter(
            user=user,
            is_primary=True,
            job_title__position__title=assignment_data
        ).exists()

    return True


def get_available_transitions(request_obj):
    if not request_obj.current_state_id:
        return Transition.objects.none()

    return Transition.objects.filter(
        workflow=request_obj.current_state.workflow,
        from_state=request_obj.current_state
    ).select_related(
        'from_state',
        'to_state',
        'workflow'
    )


@transaction.atomic
def start_request(request_obj, workflow):
    if request_obj.current_state_id:
        raise ValidationError(
            f"Request {request_obj.pk} already has a current state."
        )

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
    if not request_obj.current_state_id:
        raise ValidationError(
            f"Request {request_obj.pk} does not have a current state."
        )

    if transition.workflow_id != request_obj.current_state.workflow_id:
        raise ValidationError(
            "Transition does not belong to the current request workflow."
        )

    if request_obj.current_state_id != transition.from_state_id:
        raise ValidationError(
            f"Transition '{transition.name}' is not valid for request "
            f"{request_obj.pk} in current state '{request_obj.current_state.name}'."
        )

    if not can_user_execute_transition(request_obj, transition, performed_by):
        raise ValidationError(
            f"User '{performed_by}' is not allowed to execute "
            f"transition '{transition.name}'."
        )

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
