# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0016_remove_teaser_cpc'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaser',
            name='image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/'),
        ),
    ]
