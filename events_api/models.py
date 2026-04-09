from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    images = models.ImageField(upload_to='event_images/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name