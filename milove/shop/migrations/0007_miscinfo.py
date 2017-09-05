# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_show_on_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion', models.CharField(max_length=200, verbose_name='promotion message')),
            ],
            options={
                'verbose_name': 'misc information',
            },
        ),
    ]