from django.contrib import admin

from .models import Request, RequestTransitionLog, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    readonly_fields = ("completed_at",)


class RequestTransitionLogInline(admin.TabularInline):
    model = RequestTransitionLog
    extra = 0
    readonly_fields = ("transition", "from_state", "to_state", "performed_by", "comment", "created_at")
    can_delete = False


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "form", "creator", "current_state", "created_at", "updated_at")
    list_filter = ("form", "current_state", "created_at")
    search_fields = ("id", "creator__username", "form__title")
    readonly_fields = ("created_at", "updated_at")
    inlines = [TaskInline, RequestTransitionLogInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "assignee", "state", "is_completed", "completed_at")
    list_filter = ("is_completed", "state")
    search_fields = ("request__id", "assignee__username")


@admin.register(RequestTransitionLog)
class RequestTransitionLogAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "transition", "from_state", "to_state", "performed_by", "created_at")
    list_filter = ("from_state", "to_state", "created_at")
    search_fields = ("request__id", "performed_by__username", "comment")
    readonly_fields = ("created_at",)
