# Generated by Django 4.0.3 on 2022-08-19 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20, null=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20, null=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('unit_abbreviation', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=200, null=True, unique=True)),
                ('phone', models.CharField(max_length=200, null=True, unique=True)),
                ('profile_pic', models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_images')),
                ('bio', models.CharField(blank=True, max_length=100, null=True)),
                ('client', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('product_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('total_quantity', models.PositiveBigIntegerField(default=0, null=True)),
                ('stock_alert', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=20, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('sales_quantity', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('purchase_quantity', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('sales_created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('purchase_created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_note', models.TextField(blank=True, max_length=300, null=True)),
                ('purchase_note', models.TextField(blank=True, max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(blank=True, default=system.models.get_default_brand, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.brand')),
                ('category', models.ForeignKey(default=system.models.get_default_category, on_delete=django.db.models.deletion.CASCADE, to='system.category')),
                ('customer', models.ForeignKey(blank=True, default=system.models.get_walkin_customer, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.customer')),
                ('product_unit', models.ForeignKey(default=system.models.get_default_product_unit, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.unit')),
                ('supplier', models.ForeignKey(blank=True, default=system.models.get_generic_supplier, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.supplier')),
            ],
        ),
    ]