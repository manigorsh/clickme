# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0005_auto_20171111_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='target_language',
        ),
        migrations.DeleteModel(
            name='TargetLanguage',
        ),
    ]
