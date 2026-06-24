from django.contrib import admin
from .models import FormDefinition, FormVersion, FormField, FormFieldOption

class FormFieldOptionInline(admin.TabularInline):
    model = FormFieldOption
    extra = 1

class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    show_change_link = True

class FormVersionInline(admin.TabularInline):
    model = FormVersion
    extra = 1
    show_change_link = True

@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    search_fields = ('name', 'slug')
    inlines = [FormVersionInline]

@admin.register(FormVersion)
class FormVersionAdmin(admin.ModelAdmin):
    list_display = ('form_definition', 'version_number', 'is_published', 'created_at')
    list_filter = ('is_published', 'form_definition')
    inlines = [FormFieldInline]

@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'field_type', 'form_version', 'order', 'required')
    list_filter = ('field_type', 'form_version')
    inlines = [FormFieldOptionInline]
