from django.contrib import admin
from .models import Department, Position, JobTitle, UserAssignment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent')
    search_fields = ('name', 'code')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')
    list_filter = ('level',)

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'superior')
    
    def display_name(self, obj):
        return str(obj)
    display_name.short_description = 'Job Title'

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('user__username', 'user__email')
