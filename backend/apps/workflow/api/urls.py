from django.urls import path
from .views import InboxAPIView, ExecuteTransitionAPIView

urlpatterns = [
    path('inbox/', InboxAPIView.as_view(), name='workflow-inbox'),
    path('execute/', ExecuteTransitionAPIView.as_view(), name='workflow-execute'),
]
