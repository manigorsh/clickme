# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser', '0005_auto_20171115_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='browser',
            field=models.ManyToManyField(default=1, help_text='Select A Browser For This Campaign (default all browsers)', to='advertiser.Browser'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='device',
            field=models.ManyToManyField(default=1, help_text='Select A Device For This Campaign (default all devices)', to='advertiser.Device'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='geo',
            field=models.ManyToManyField(default=1, help_text='Select A Geo For This Campaign (default all geos)', to='advertiser.Geo'),
        ),
    ]