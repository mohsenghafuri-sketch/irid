from rest_framework import serializers
from .models import Letter, DocumentType, LetterRecipient
from apps.accounts.api.serializers import UserMeSerializer

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'title', 'code']

class LetterSerializer(serializers.ModelSerializer):
    # استفاده از UserMeSerializer طبق ساختار موجود در پروژه
    sender_details = UserMeSerializer(source='sender', read_only=True)
    document_type_details = DocumentTypeSerializer(source='document_type', read_only=True)

    class Meta:
        model = Letter
        fields = [
            'id', 'title', 'content', 'indicator_number',
            'sender', 'sender_details', 'priority', 'classification',
            'document_type', 'document_type_details', 'created_at'
        ]
        read_only_fields = ['indicator_number', 'sender']

    def create(self, validated_data):
        import uuid
        if not validated_data.get('indicator_number'):
            validated_data['indicator_number'] = f"LTR-{uuid.uuid4().hex[:6].upper()}"
        
        # هندل کردن فرستنده از طریق Context درخواست
        if 'request' in self.context:
            validated_data['sender'] = self.context['request'].user
            
        return super().create(validated_data)
