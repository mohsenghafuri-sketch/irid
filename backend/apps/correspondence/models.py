from django.db import models
from django.conf import settings


class DocumentType(models.Model):
    """انواع سند: نامه، حکم، صورتجلسه و غیره"""
    title = models.CharField(max_length=100)
    code = models.SlugField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نوع سند"
        verbose_name_plural = "انواع سند"


class Letter(models.Model):
    """مدل اصلی نامه"""

    class Priority(models.TextChoices):
        NORMAL = "normal", "عادی"
        URGENT = "urgent", "فوری"
        IMMEDIATE = "immediate", "آنی"

    class Classification(models.TextChoices):
        PUBLIC = "public", "عادی"
        CONFIDENTIAL = "confidential", "محرمانه"
        SECRET = "secret", "سری"

    title = models.CharField(max_length=500, verbose_name="موضوع")
    content = models.TextField(verbose_name="متن نامه")
    indicator_number = models.CharField(max_length=100, unique=True, verbose_name="شماره اندیکاتور")

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sent_letters",
        verbose_name="فرستنده",
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
        verbose_name="فوریت",
    )

    classification = models.CharField(
        max_length=20,
        choices=Classification.choices,
        default=Classification.PUBLIC,
        verbose_name="طبقه‌بندی",
    )

    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="نوع سند",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    def __str__(self):
        return f"{self.indicator_number} - {self.title}"

    class Meta:
        verbose_name = "نامه"
        verbose_name_plural = "نامه‌ها"
        ordering = ["-created_at"]


class LetterRecipient(models.Model):
    """گیرندگان نامه و وضعیت مشاهده"""

    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="نامه",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="گیرنده",
    )
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان خواندن")

    class Meta:
        verbose_name = "گیرنده نامه"
        verbose_name_plural = "گیرندگان نامه"
        unique_together = ("letter", "user")

    def __str__(self):
        return f"{self.letter} -> {self.user}"

