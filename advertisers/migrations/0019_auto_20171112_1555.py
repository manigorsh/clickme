# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0018_auto_20171112_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaser',
            name='image',
            field=models.ImageField(default='teasers/no-image-icon.png', upload_to='teasers/'),
        ),
    ]
