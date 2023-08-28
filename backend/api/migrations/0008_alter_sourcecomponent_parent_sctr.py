# Generated by Django 4.2.3 on 2023-08-23 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_sctr_sourcecomponent_remove_subcomponent_main_sku_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcecomponent',
            name='parent_sctr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='api.sctr'),
        ),
    ]
