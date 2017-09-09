# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-09 07:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20170905_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='created datetime')),
                ('amount', models.FloatField(verbose_name='Withdrawal|amount')),
                ('processed_amount', models.FloatField(default=0.0, verbose_name='Withdrawal|processed amount')),
                ('method', models.CharField(choices=[('paypal', 'PayPal'), ('alipay', 'Alipay'), ('other', 'Other')], max_length=20, verbose_name='Withdrawal|method')),
                ('vendor_account', models.CharField(max_length=200, verbose_name='Withdrawal|vendor account')),
                ('status', models.CharField(choices=[('pending', 'WithdrawalStatus|pending'), ('closed', 'WithdrawalStatus|closed'), ('done', 'WithdrawalStatus|done')], default='pending', max_length=20, verbose_name='status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='withdrawals', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'withdrawal',
                'verbose_name_plural': 'withdrawals',
            },
        ),
    ]
