from django.contrib import admin
from .models import Department, Position, JobTitle, UserAssignment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'superior')

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'is_primary')
