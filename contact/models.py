from django.db import models

# Create your models here.
# app/models.py
class Contact(models.Model):
    unique_id = models.CharField(unique=True)
    contact_name = models.CharField(max_length=255)
    greeting_name = models.CharField(max_length=255)

    def __str__(self):
        return self.contact_name
