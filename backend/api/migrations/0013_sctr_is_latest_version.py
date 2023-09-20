# Generated by Django 4.2.4 on 2023-09-07 12:57

from django.db import migrations, models

def set_latest_version_flag(apps, schema_editor):
    """Set is_latest_version to True for SCTRs if have the latest version."""
    model = apps.get_model('api', 'SCTR')

    for unique_identifier in model.objects.values('unique_identifier').distinct():
        latest_version = model.objects.filter(unique_identifier=unique_identifier['unique_identifier']).order_by('-version').first()

        if latest_version:
            model.objects.filter(pk=latest_version.pk).update(is_latest_version=True)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_sctr_unique_identifier_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sctr',
            name='is_latest_version',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(set_latest_version_flag),
    ]