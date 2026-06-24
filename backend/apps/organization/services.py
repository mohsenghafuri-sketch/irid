from __future__ import annotations

from typing import Optional

from django.contrib.auth import get_user_model

from .models import UserAssignment, JobTitle

User = get_user_model()


def get_primary_assignment(user) -> Optional[UserAssignment]:
    if user is None:
        return None

    return (
        UserAssignment.objects
        .select_related("job_title", "job_title__department", "job_title__position", "job_title__superior")
        .filter(user=user, is_primary=True)
        .order_by("id")
        .first()
    )


def get_direct_superior_job_title(user) -> Optional[JobTitle]:
    assignment = get_primary_assignment(user)
    if assignment is None:
        return None

    return assignment.job_title.superior


def get_direct_superior_assignment(user) -> Optional[UserAssignment]:
    superior_job_title = get_direct_superior_job_title(user)
    if superior_job_title is None:
        return None

    assignment = (
        UserAssignment.objects
        .select_related("user", "job_title", "job_title__department", "job_title__position")
        .filter(job_title=superior_job_title, is_primary=True)
        .order_by("id")
        .first()
    )
    if assignment is not None:
        return assignment

    return (
        UserAssignment.objects
        .select_related("user", "job_title", "job_title__department", "job_title__position")
        .filter(job_title=superior_job_title)
        .order_by("id")
        .first()
    )


def get_direct_superior_user(user):
    assignment = get_direct_superior_assignment(user)
    if assignment is None:
        return None
    return assignment.user
