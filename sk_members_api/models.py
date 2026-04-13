from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)

    age = models.IntegerField(default=0, null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    sk_picture = models.ImageField(upload_to='sk_pictures/', blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

