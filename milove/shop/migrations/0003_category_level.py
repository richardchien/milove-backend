# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20170904_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=1, editable=False, verbose_name='category level'),
            preserve_default=False,
        ),
    ]