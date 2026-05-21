from django.db import models



class Member(models.Model):
    CHOICES = [
        ('SK Chairperson', 'SK Chairperson'),
        ('SK Secretary', 'SK Secretary'),
        ('SK Treasurer', 'SK Treasurer'),
        ('SK Councilor 1', 'SK Councilor 1'),
        ('SK Councilor 2', 'SK Councilor 2'),
        ('SK Councilor 3', 'SK Councilor 3'),
        ('SK Councilor 4', 'SK Councilor 4'),
        ('SK Councilor 5', 'SK Councilor 5'),
        ('SK Councilor 6', 'SK Councilor 6'),
        ('SK Councilor 7', 'SK Councilor 7'),
    ]
    
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)

    age = models.IntegerField(default=0, null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    sk_picture = models.ImageField(upload_to='sk_pictures/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

