from django.db import models
import datetime

# Create your models here.

class Email(models.Model):
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=264)
    message = models.CharField(max_length=1000)
    date = models.DateField()

    def __str__(self):
        return self.email + ' ' + self.subject
