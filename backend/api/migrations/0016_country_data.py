# Generated by Django 4.2.5 on 2023-09-23 15:21

from django.db import migrations, models
from pycountry import countries

class Migration(migrations.Migration):
    atomic = True

    dependencies = [
        ("api", "0015_country"),
    ]


    def load_countries(apps, schema_editor):
        Country = apps.get_model("api", "Country")

        for pyc in list(countries):
            country = Country(
                alpha_2 = pyc.alpha_2,
                alpha_3 = pyc.alpha_3,
                name = pyc.name,
                official_name = pyc.official_name if hasattr(pyc, 'official_name') else pyc.name,
                free = True)
            country.save()

    def delete_countries(apps, schema_editor):
        Country = apps.get_model("api", "Country")
        Country.objects.all().delete()


    operations = [
        migrations.RunPython(load_countries, delete_countries),
    ]