from django.urls import path
from .views import FormDefinitionListView

urlpatterns = [
    path('', FormDefinitionListView.as_view(), name='form-definition-list'),
]
