from django.db import models
from django.conf import settings
from apps.forms.models import FormVersion
from apps.workflow.models import State

class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requests')
    form_version = models.ForeignKey(FormVersion, on_delete=models.PROTECT)
    
    # اتصال به موتور گردش کار
    current_state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True, related_name='current_requests')
    
    tracking_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.id} - {self.current_state.name if self.current_state else 'No State'}"

class RequestValue(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='data')
    values = models.JSONField(default=dict)

class RequestHistory(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='history')
    from_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+')
    to_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+')
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    action_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
