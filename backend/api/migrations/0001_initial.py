# Generated by Django 4.2.3 on 2023-08-08 13:01

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_website', models.URLField(unique=True)),
                ('company_name', models.CharField(max_length=200)),
                ('company_jurisdiction', models.CharField(max_length=400, null=True)),
                ('company_headquarters_physical_address', models.CharField(max_length=400, null=True)),
                ('company_unique_identifier', models.FileField(null=True, upload_to='company_identifiers/%Y/%m')),
                ('industry', models.CharField(max_length=50, null=True)),
                ('company_size', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('company_phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.IntegerField(unique=True)),
                ('public_facing_id', models.IntegerField()),
                ('public_facing_name', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=2000)),
                ('sctr_date', models.DateField()),
                ('sctr_cogs', models.FloatField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('cogs_coutry_recipients', django_countries.fields.CountryField(max_length=2)),
                ('product_input_manufacturer', models.CharField(max_length=200)),
                ('product_input_type', models.CharField(choices=[('Convenience Goods', 'Convenience Goods'), ('Raw Materials', 'Raw Materials'), ('Component Parts', 'Component Parts'), ('Software', 'Software'), ('Hardware', 'Hardware'), ('Consumer Electronics', 'Consumer Electronics'), ('Cookware', 'Cookware'), ('Appliances', 'Appliances'), ('Homegoods', 'Homegoods'), ('Clothing', 'Clothing'), ('Jewelry', 'Jewelry'), ('Art', 'Art')], max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='SubComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_sku_id', models.IntegerField()),
                ('sub_public_facing_name', models.CharField(max_length=500, null=True)),
                ('sub_cogs_coutry_recipients', django_countries.fields.CountryField(max_length=2, null=True)),
                ('sub_product_input_type', models.CharField(choices=[('Convenience Goods', 'Convenience Goods'), ('Raw Materials', 'Raw Materials'), ('Component Parts', 'Component Parts'), ('Software', 'Software'), ('Hardware', 'Hardware'), ('Consumer Electronics', 'Consumer Electronics'), ('Cookware', 'Cookware'), ('Appliances', 'Appliances'), ('Homegoods', 'Homegoods'), ('Clothing', 'Clothing'), ('Jewelry', 'Jewelry'), ('Art', 'Art')], max_length=20, null=True)),
                ('main_sku_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.company')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
