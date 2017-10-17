from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    age = models.DecimalField(max_digits=3, decimal_places=2)
    gender = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    imgUrl = models.SlugField()
    rank = models.CharField(max_length=1000)
