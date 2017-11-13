# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 09:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publisher', '0002_auto_20171113_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epayments_wallet', models.CharField(help_text='Enter a Epayments Wallet Number (e.g. xxx-xxxxxx)', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='widget',
            options={'ordering': ['impressions']},
        ),
    ]
