# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='advertisers.Status'),
        ),
    ]