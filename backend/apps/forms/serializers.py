from rest_framework import serializers
from .models import FormDefinition

class FormDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDefinition
        fields = '__all__'
