from django.db import models

class Student(models.Model):
    Name = models.CharField(max_length=255)
    Class = models.CharField(max_length=255)
    School = models.CharField(max_length=255)
    State = models.CharField(max_length=255)