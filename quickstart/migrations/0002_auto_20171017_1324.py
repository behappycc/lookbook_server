# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(max_length=4),
        ),
    ]
