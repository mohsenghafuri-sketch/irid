from django.contrib import admin
from .models import FormDefinition

@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at')
    search_fields = ('title', 'slug')
