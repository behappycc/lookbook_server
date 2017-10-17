from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    age = models.CharField(max_length=4)
    gender = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    imgUrl = models.SlugField()
    rank = models.CharField(max_length=1000)
