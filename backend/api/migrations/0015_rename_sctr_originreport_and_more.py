# Generated by Django 4.2.5 on 2023-09-27 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_sourcecomponent_company_name"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SCTR",
            new_name="OriginReport",
        ),
        migrations.RenameField(
            model_name="sourcecomponent",
            old_name="parent_sctr",
            new_name="parent_origin_report",
        ),
    ]
