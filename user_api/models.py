from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        COLLECTOR = "collector", "Collector"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, blank=True, null=True, choices=RoleChoices.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
