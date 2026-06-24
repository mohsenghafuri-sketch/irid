from django.contrib import admin
from .models import Workflow, State, Transition

class StateInline(admin.TabularInline):
    model = State
    extra = 1

class TransitionInline(admin.TabularInline):
    model = Transition
    fk_name = 'workflow'
    extra = 1

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    inlines = [StateInline, TransitionInline]

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'workflow', 'is_initial', 'is_final')
    list_filter = ('workflow', 'is_initial', 'is_final')

@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'workflow', 'from_state', 'to_state', 'assignment_type')
    list_filter = ('workflow', 'assignment_type')
