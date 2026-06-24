from django.contrib import admin
from .models import Request, RequestValue, RequestHistory

class RequestValueInline(admin.StackedInline):
    model = RequestValue
    can_delete = False

class RequestHistoryInline(admin.TabularInline):
    model = RequestHistory
    extra = 0
    readonly_fields = ('from_state', 'to_state', 'performed_by', 'action_name', 'created_at')
    can_delete = False

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'form_version', 'get_state_name', 'tracking_code', 'created_at')
    list_filter = ('current_state', 'form_version', 'created_at')
    search_fields = ('tracking_code', 'user__email')
    inlines = [RequestValueInline, RequestHistoryInline]

    def get_state_name(self, obj):
        return obj.current_state.name if obj.current_state else "نامشخص"
    get_state_name.short_description = 'وضعیت فعلی'

@admin.register(RequestHistory)
class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = ('request', 'from_state', 'to_state', 'performed_by', 'action_name', 'created_at')
