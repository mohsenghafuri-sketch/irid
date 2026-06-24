from rest_framework import viewsets, permissions
from django.db import models
from .models import Letter, DocumentType
from .serializers import LetterSerializer, DocumentTypeSerializer

class LetterViewSet(viewsets.ModelViewSet):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # فیلتر برای نمایش نامه‌هایی که کاربر فرستنده یا گیرنده آن‌هاست
        return Letter.objects.filter(
            models.Q(sender=user) | models.Q(recipients__user=user)
        ).distinct()

class DocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
