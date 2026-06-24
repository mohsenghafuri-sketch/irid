from django.db import transaction
from django.utils import timezone

from apps.forms.models import FormDefinition
from apps.workflow.models import Transition, Workflow
from .models import Request, RequestTransitionLog, Task


class BPMSEngine:
    @staticmethod
    @transaction.atomic
    def create_request(form_slug, creator, data, initial_assignee=None):
        form_def = FormDefinition.objects.get(slug=form_slug, is_active=True)
        workflow = Workflow.objects.get(form=form_def)
        initial_state = workflow.states.get(is_initial=True)

        request_obj = Request.objects.create(
            form=form_def,
            creator=creator,
            data=data,
            current_state=initial_state,
        )

        Task.objects.create(
            request=request_obj,
            assignee=initial_assignee or creator,
            state=initial_state,
        )

        return request_obj

    @staticmethod
    @transaction.atomic
    def apply_transition(request_obj, transition_id, user, next_assignee=None, comment=""):
        transition = Transition.objects.select_related(
            "from_state",
            "to_state",
            "workflow",
        ).get(
            id=transition_id,
            workflow=request_obj.current_state.workflow,
            from_state=request_obj.current_state,
        )

        if transition.permission_required and not user.has_perm(transition.permission_required):
            raise PermissionError(f"User does not have permission: {transition.permission_required}")

        old_state = request_obj.current_state
        new_state = transition.to_state

        Task.objects.filter(
            request=request_obj,
            state=old_state,
            is_completed=False,
        ).update(
            is_completed=True,
            completed_at=timezone.now(),
            comment=comment,
        )

        RequestTransitionLog.objects.create(
            request=request_obj,
            transition=transition,
            from_state=old_state,
            to_state=new_state,
            performed_by=user,
            comment=comment,
        )

        request_obj.current_state = new_state
        request_obj.save(update_fields=["current_state", "updated_at"])

        if not new_state.is_final:
            Task.objects.create(
                request=request_obj,
                assignee=next_assignee or request_obj.creator,
                state=new_state,
            )

        return request_obj
