# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0004_auto_20171115_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]