from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_departments')
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=255)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class JobTitle(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_titles')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='job_titles')
    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    class Meta:
        unique_together = ('department', 'position')

    def __str__(self):
        return f"{self.position.title} - {self.department.name}"

class UserAssignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'job_title')
