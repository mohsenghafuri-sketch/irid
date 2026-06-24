from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LetterViewSet, DocumentTypeViewSet

router = DefaultRouter()
router.register(r'letters', LetterViewSet)
router.register(r'document-types', DocumentTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
