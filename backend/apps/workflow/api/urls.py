from django.urls import path
from .views import InboxAPIView

urlpatterns = [
    path('inbox/', InboxAPIView.as_view(), name='workflow-inbox'),
]
