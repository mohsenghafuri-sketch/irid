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
    list_display = ('name', 'form')
    inlines = [StateInline, TransitionInline]

admin.site.register(State)
admin.site.register(Transition)
