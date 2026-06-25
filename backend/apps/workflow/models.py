from django.db import models

class Workflow(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام گردش کار")
    code = models.SlugField(max_length=100, unique=True, verbose_name="کد سیستم")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class State(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100, verbose_name="نام وضعیت")
    code = models.SlugField(max_length=100, verbose_name="کد وضعیت")
    is_initial = models.BooleanField(default=False, verbose_name="وضعیت شروع")
    is_final = models.BooleanField(default=False, verbose_name="وضعیت نهایی")

    class Meta:
        unique_together = ('workflow', 'code')

    def __str__(self):
        return f"{self.workflow.name} -> {self.name}"

class Transition(models.Model):
    ASSIGNMENT_TYPES = (
        ('DIRECT_MANAGER', 'مدیر مستقیم درخواست‌کننده'),
        ('SPECIFIC_USER', 'کاربر مشخص'),
        ('ROLE', 'نقش سیستمی (مثلاً مدیر مالی)'),
        ('CREATOR', 'خود درخواست‌کننده'),
    )

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='transitions')
    name = models.CharField(max_length=100, verbose_name="نام عملیات")
    from_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='out_transitions')
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='in_transitions')
    
    assignment_type = models.CharField(max_length=50, choices=ASSIGNMENT_TYPES, default='DIRECT_MANAGER')
    # فیلد کمکی برای نقش‌ها یا کاربران خاص
    assignment_data = models.CharField(max_length=255, null=True, blank=True, help_text="ID کاربر یا کد نقش")

    def __str__(self):
        return f"{self.name} ({self.from_state.name} -> {self.to_state.name})"

class ActionLog(models.Model):
    request = models.ForeignKey('requests.Request', on_delete=models.CASCADE, related_name='action_logs')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, verbose_name='انجام دهنده')
    transition = models.ForeignKey(Transition, on_delete=models.SET_NULL, null=True, verbose_name='عملیات')
    from_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name='وضعیت قبلی')
    to_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name='وضعیت جدید')
    comment = models.TextField(blank=True, null=True, verbose_name='توضیحات/هامش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')

    class Meta:
        verbose_name = 'لاگ عملیات'
        verbose_name_plural = 'لاگ‌های عملیات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.request} - {self.transition}'

class ActionLog(models.Model):
    request = models.ForeignKey('requests.Request', on_delete=models.CASCADE, related_name='action_logs')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, verbose_name='انجام دهنده')
    transition = models.ForeignKey(Transition, on_delete=models.SET_NULL, null=True, verbose_name='عملیات')
    from_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name='وضعیت قبلی')
    to_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='+', verbose_name='وضعیت جدید')
    comment = models.TextField(blank=True, null=True, verbose_name='توضیحات/هامش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')

    class Meta:
        verbose_name = 'لاگ عملیات'
        verbose_name_plural = 'لاگ‌های عملیات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.request} - {self.transition}'
