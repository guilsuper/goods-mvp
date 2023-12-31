# Generated by Django 4.2.3 on 2023-08-21 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_company_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrator',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_headquarters_physical_address',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_phonenumber',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_size',
        ),
        migrations.RemoveField(
            model_name='company',
            name='industry',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='company_website',
            new_name='website',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='company_jurisdiction',
            new_name='jurisdiction',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='company_name',
            new_name='name',
        ),
    ]
