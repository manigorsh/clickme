# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0003_auto_20171113_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget',
            name='columns',
        ),
        migrations.RemoveField(
            model_name='widget',
            name='rows',
        ),
    ]
