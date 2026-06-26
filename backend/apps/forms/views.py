from rest_framework import generics, permissions
from .models import FormDefinition
from .serializers import FormDefinitionSerializer

class FormDefinitionListView(generics.ListAPIView):
    queryset = FormDefinition.objects.all()
    serializer_class = FormDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
