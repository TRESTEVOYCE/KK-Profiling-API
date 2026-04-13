from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('collector', 'Collector'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='collector')

    def __str__(self):
        return self.user.username


