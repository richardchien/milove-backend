# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 08:15
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.password_validation
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import milove.shop.models.product
import milove.shop.models.sell_request
import milove.shop.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.', max_length=150, unique=True, validators=[milove.shop.validators.UsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email address already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password], verbose_name='password')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, verbose_name='Address|fullname')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('country', models.CharField(choices=[('US', 'United State'), ('CA', 'Canada')], max_length=3, verbose_name='Address|country')),
                ('street_address', models.CharField(max_length=200, verbose_name='Address|street address')),
                ('city', models.CharField(max_length=100, verbose_name='Address|city')),
                ('province', models.CharField(max_length=100, verbose_name='Address|province')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Address|ZIP code')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, verbose_name='Address|fullname')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('country', models.CharField(choices=[('US', 'United State'), ('CA', 'Canada')], max_length=3, verbose_name='Address|country')),
                ('street_address', models.CharField(max_length=200, verbose_name='Address|street address')),
                ('city', models.CharField(max_length=100, verbose_name='Address|city')),
                ('province', models.CharField(max_length=100, verbose_name='Address|province')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Address|ZIP code')),
            ],
            options={
                'verbose_name': 'billing address',
                'verbose_name_plural': 'billing addresses',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('super_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.Category', verbose_name='super category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Coupon|code')),
                ('type', models.CharField(choices=[('rate', 'Coupon|rate'), ('amount', 'Coupon|amount')], default='rate', max_length=10, verbose_name='type')),
                ('price_required', models.FloatField(default=0.0, verbose_name='Coupon|price required')),
                ('discount', models.FloatField(verbose_name='Coupon|discount')),
                ('is_valid', models.BooleanField(default=True, verbose_name='Coupon|is valid')),
            ],
            options={
                'verbose_name': 'coupon',
                'verbose_name_plural': 'coupons',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='created datetime')),
                ('total_price', models.FloatField(verbose_name='total price')),
                ('discount_amount', models.FloatField(blank=True, default=0.0, verbose_name='discount amount')),
                ('paid_amount', models.FloatField(blank=True, default=0.0, verbose_name='paid amount')),
                ('comment', models.TextField(blank=True, verbose_name='Order|comment')),
                ('status', models.CharField(choices=[('unpaid', 'OrderStatus|unpaid'), ('closed', 'OrderStatus|closed'), ('paid', 'OrderStatus|paid'), ('cancelling', 'OrderStatus|cancelling'), ('cancelled', 'OrderStatus|cancelled'), ('shipping', 'OrderStatus|shipping'), ('done', 'OrderStatus|done'), ('return-requested', 'OrderStatus|return requested'), ('returning', 'OrderStatus|returning'), ('returned', 'OrderStatus|returned')], default='unpaid', max_length=20, verbose_name='status')),
                ('last_status', models.CharField(blank=True, choices=[('unpaid', 'OrderStatus|unpaid'), ('closed', 'OrderStatus|closed'), ('paid', 'OrderStatus|paid'), ('cancelling', 'OrderStatus|cancelling'), ('cancelled', 'OrderStatus|cancelled'), ('shipping', 'OrderStatus|shipping'), ('done', 'OrderStatus|done'), ('return-requested', 'OrderStatus|return requested'), ('returning', 'OrderStatus|returning'), ('returned', 'OrderStatus|returned')], max_length=20, null=True, verbose_name='last status')),
                ('express_company', models.CharField(blank=True, max_length=60, null=True, verbose_name='express company')),
                ('tracking_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='tracking number')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'permissions': (('randomly_switch_order_status', 'Can randomly switch order status'),),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='strike price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusTransition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happened_dt', models.DateTimeField(auto_now_add=True, verbose_name='happened datetime')),
                ('src_status', models.CharField(choices=[('unpaid', 'OrderStatus|unpaid'), ('closed', 'OrderStatus|closed'), ('paid', 'OrderStatus|paid'), ('cancelling', 'OrderStatus|cancelling'), ('cancelled', 'OrderStatus|cancelled'), ('shipping', 'OrderStatus|shipping'), ('done', 'OrderStatus|done'), ('return-requested', 'OrderStatus|return requested'), ('returning', 'OrderStatus|returning'), ('returned', 'OrderStatus|returned')], max_length=20, verbose_name='source status')),
                ('dst_status', models.CharField(choices=[('unpaid', 'OrderStatus|unpaid'), ('closed', 'OrderStatus|closed'), ('paid', 'OrderStatus|paid'), ('cancelling', 'OrderStatus|cancelling'), ('cancelled', 'OrderStatus|cancelled'), ('shipping', 'OrderStatus|shipping'), ('done', 'OrderStatus|done'), ('return-requested', 'OrderStatus|return requested'), ('returning', 'OrderStatus|returning'), ('returned', 'OrderStatus|returned')], max_length=20, verbose_name='destination status')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_transitions', to='shop.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order status transition',
                'verbose_name_plural': 'order status transitions',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='created datetime')),
                ('amount', models.FloatField(verbose_name='Payment|amount')),
                ('use_balance', models.BooleanField(verbose_name='Payment|use balance')),
                ('amount_from_balance', models.FloatField(default=0.0, verbose_name='Payment|amount from balance')),
                ('paid_amount_from_balance', models.FloatField(default=0.0, verbose_name='Payment|paid amount from balance')),
                ('use_point', models.BooleanField(verbose_name='Payment|use point')),
                ('amount_from_point', models.FloatField(default=0.0, verbose_name='Payment|amount from point')),
                ('paid_point', models.IntegerField(default=0, verbose_name='Payment|paid point')),
                ('method', models.CharField(blank=True, choices=[('paypal', 'PayPal'), ('credit-card', 'credit card')], max_length=20, null=True, verbose_name='Payment|method')),
                ('vendor_payment_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment|vendor payment ID')),
                ('extra_info', jsonfield.fields.JSONField(blank=True, default={}, verbose_name='extra information')),
                ('status', models.CharField(choices=[('pending', 'PaymentStatus|pending'), ('closed', 'PaymentStatus|closed'), ('failed', 'PaymentStatus|failed'), ('succeeded', 'PaymentStatus|succeeded')], default='pending', max_length=20, verbose_name='status')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='shop.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('method', models.CharField(choices=[('credit-card', 'credit card')], max_length=20, verbose_name='PaymentMethod|method')),
                ('info', jsonfield.fields.JSONField(blank=True, default={}, verbose_name='PaymentMethod|information')),
                ('secret', jsonfield.fields.JSONField(blank=True, default={}, verbose_name='PaymentMethod|secret information')),
            ],
            options={
                'verbose_name': 'payment method',
                'verbose_name_plural': 'payment methods',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_dt', models.DateTimeField(auto_now_add=True, verbose_name='Product|published datetime')),
                ('sold', models.BooleanField(default=False, verbose_name='Product|sold')),
                ('sold_dt', models.DateTimeField(blank=True, null=True, verbose_name='Product|sold datetime')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Product|name')),
                ('style', models.CharField(blank=True, max_length=200, verbose_name='Product|style')),
                ('size', models.CharField(blank=True, max_length=20, verbose_name='Product|size')),
                ('condition', models.CharField(choices=[('S', 'ProductCondition|S'), ('A+', 'ProductCondition|A+'), ('A', 'ProductCondition|A'), ('B', 'ProductCondition|B'), ('C', 'ProductCondition|C'), ('D', 'ProductCondition|D')], max_length=2, verbose_name='Product|condition')),
                ('description', models.TextField(blank=True, verbose_name='Product|description')),
                ('original_price', models.FloatField(verbose_name='Product|original price')),
                ('buy_back_price', models.FloatField(blank=True, null=True, verbose_name='Product|buy back price')),
                ('price', models.FloatField(verbose_name='Product|price')),
                ('main_image', models.ImageField(default='placeholders/120x120.png', upload_to=milove.shop.models.product._prod_image_path, verbose_name='Product|main image')),
                ('attachments', models.ManyToManyField(blank=True, to='shop.Attachment', verbose_name='Product|attachments')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Brand', verbose_name='Product|brand')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='shop.Category', verbose_name='Product|categories')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=milove.shop.models.product._prod_image_path, verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
        ),
        migrations.CreateModel(
            name='SellRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='created datetime')),
                ('brand', models.CharField(max_length=100, verbose_name='Product|brand')),
                ('category', models.CharField(max_length=30, verbose_name='Product|category')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Product|name')),
                ('size', models.CharField(blank=True, max_length=20, verbose_name='Product|size')),
                ('condition', models.CharField(max_length=100, verbose_name='Product|condition')),
                ('purchase_year', models.CharField(max_length=10, verbose_name='SellRequest|purchase year')),
                ('original_price', models.FloatField(verbose_name='Product|original price')),
                ('attachments', models.CharField(blank=True, max_length=200, verbose_name='Product|attachments')),
                ('description', models.TextField(blank=True, verbose_name='Product|description')),
                ('image_paths', jsonfield.fields.JSONField(blank=True, default=[], verbose_name='image paths')),
                ('status', models.CharField(choices=[('created', 'SellRequest|created'), ('cancelled', 'SellRequest|cancelled'), ('denied', 'SellRequest|denied'), ('valuated', 'SellRequest|valuated'), ('closed', 'SellRequest|closed'), ('decided', 'SellRequest|decided'), ('shipping', 'SellRequest|shipping'), ('authenticating', 'SellRequest|authenticating'), ('selling', 'SellRequest|selling'), ('done', 'SellRequest|done')], default='created', max_length=20, verbose_name='status')),
                ('denied_reason', models.TextField(blank=True, null=True, verbose_name='SellRequest|denied reason')),
                ('buy_back_valuation', models.FloatField(blank=True, null=True, verbose_name='SellRequest|buy back valuation')),
                ('sell_valuation', models.FloatField(blank=True, null=True, verbose_name='SellRequest|sell valuation')),
                ('valuated_dt', models.DateTimeField(blank=True, null=True, verbose_name='SellRequest|valuated datetime')),
                ('sell_type', models.CharField(blank=True, choices=[('buy-back', 'SellRequest|buy back'), ('sell', 'SellRequest|sell')], max_length=20, null=True, verbose_name='SellRequest|sell type')),
                ('shipping_label', models.FileField(blank=True, null=True, upload_to=milove.shop.models.sell_request._shipping_label_upload_path, verbose_name='shipping label')),
                ('express_company', models.CharField(blank=True, max_length=60, null=True, verbose_name='express company')),
                ('tracking_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='tracking number')),
            ],
            options={
                'verbose_name': 'sell request',
                'verbose_name_plural': 'sell requests',
            },
        ),
        migrations.CreateModel(
            name='SellRequestSenderAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, verbose_name='Address|fullname')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('country', models.CharField(choices=[('US', 'United State'), ('CA', 'Canada')], max_length=3, verbose_name='Address|country')),
                ('street_address', models.CharField(max_length=200, verbose_name='Address|street address')),
                ('city', models.CharField(max_length=100, verbose_name='Address|city')),
                ('province', models.CharField(max_length=100, verbose_name='Address|province')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Address|ZIP code')),
                ('sell_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sender_address', to='shop.SellRequest', verbose_name='sell request')),
            ],
            options={
                'verbose_name': 'sell request sender address',
                'verbose_name_plural': 'sell request sender addresses',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, verbose_name='Address|fullname')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('country', models.CharField(choices=[('US', 'United State'), ('CA', 'Canada')], max_length=3, verbose_name='Address|country')),
                ('street_address', models.CharField(max_length=200, verbose_name='Address|street address')),
                ('city', models.CharField(max_length=100, verbose_name='Address|city')),
                ('province', models.CharField(max_length=100, verbose_name='Address|province')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Address|ZIP code')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='shop.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'shipping address',
                'verbose_name_plural': 'shipping addresses',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='info', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('balance', models.FloatField(default=0.0, verbose_name='UserInfo|balance')),
                ('point', models.IntegerField(default=0, verbose_name='UserInfo|point')),
                ('contact', jsonfield.fields.JSONField(blank=True, default={}, verbose_name='UserInfo|contact')),
            ],
            options={
                'verbose_name': 'user information',
                'verbose_name_plural': 'user information',
            },
        ),
        migrations.AddField(
            model_name='sellrequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sell_requests', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='shop.Payment', verbose_name='payment'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
