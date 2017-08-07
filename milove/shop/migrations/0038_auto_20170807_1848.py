# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_auto_20170807_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellrequest',
            name='sell_type',
            field=models.CharField(blank=True, choices=[('buy-back', 'SellRequest|buy back'), ('sell', 'SellRequest|sell')], max_length=20, null=True, verbose_name='SellRequest|sell type'),
        ),
    ]
