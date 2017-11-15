# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 08:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertiser', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('domain', models.URLField(default='')),
                ('status', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='advertiser.Status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('impressions', models.BigIntegerField(default=0)),
                ('clicks', models.BigIntegerField(default=0)),
                ('earned', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('category', models.ForeignKey(default=1, help_text='Select A Category For This Widget', on_delete=django.db.models.deletion.CASCADE, to='advertiser.Category')),
                ('geo', models.ManyToManyField(blank=True, help_text='Select A Geo For This Campaign (default all geos)', to='advertiser.Geo')),
                ('language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='widget_language', to='advertiser.Language')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publisher.Site')),
            ],
            options={
                'ordering': ['impressions'],
            },
        ),
    ]
