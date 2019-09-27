from django.db import models

# Create your models here.

class Document(models.Model):
    docfile = models.FileField(blank=True, upload_to='documents/%Y/%B/%a/Raw Data/')

class New_Document(models.Model):
    docfile = models.FileField(blank=True, upload_to='documents/%Y/%B/%a/Final Output/')
