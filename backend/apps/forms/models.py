from django.db import models
from django.utils.text import slugify

class FormDefinition(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class FormVersion(models.Model):
    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('form_definition', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.form_definition.name} - v{self.version_number}"

class FormField(models.Model):
    FIELD_TYPES = (
        ('text', 'Short Text'),
        ('textarea', 'Long Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('select', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('file', 'File Upload'),
    )

    form_version = models.ForeignKey(FormVersion, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255, help_text="Internal name for data storage")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    help_text = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.field_type})"

class FormFieldOption(models.Model):
    field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.label
