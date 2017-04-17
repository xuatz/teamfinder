# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-17 00:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tf_auth', '0007_tfuser_steamid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfuser',
            name='avatar',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Avatar URL'),
        ),
        migrations.AddField(
            model_name='tfuser',
            name='avatarfull',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Avatar URL (full)'),
        ),
    ]
