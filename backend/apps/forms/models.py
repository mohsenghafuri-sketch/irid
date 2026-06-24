from django.db import models

class FormDefinition(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان فرم")
    slug = models.SlugField(unique=True, verbose_name="شناسه یکتا")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    fields_schema = models.JSONField(default=list, verbose_name="ساختار فیلدها")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تعریف فرم"
        verbose_name_plural = "تعریف فرم‌ها"

    def __str__(self):
        return self.title
