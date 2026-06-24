from django.db import models

class Workflow(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام فرایند")
    form = models.OneToOneField('forms.FormDefinition', on_delete=models.CASCADE, related_name='workflow')
    
    class Meta:
        verbose_name = "گردش کار"
        verbose_name_plural = "گردش کارها"

class State(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100, verbose_name="نام مرحله")
    is_initial = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.workflow.name} -> {self.name}"

class Transition(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='transitions')
    from_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='outgoing')
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='incoming')
    label = models.CharField(max_length=100, verbose_name="عملیات")
    permission_required = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.label}: {self.from_state.name} -> {self.to_state.name}"
