# Generated by Django 4.2.5 on 2023-09-23 15:21

from django.db import migrations, models
from free_world_countries import countries, Status
import pycountry

class Migration(migrations.Migration):
    atomic = True

    dependencies = [
        ("api", "0016_country"),
    ]


    def load_countries(apps, schema_editor):
        Country = apps.get_model("api", "Country")

        for country in list(countries.values()):
            if country.status in [Status.NotFree, Status.Free]:
                pyc = pycountry.countries.get(alpha_2=country.alpha_2)

                Country.objects.create(
                    alpha_2 = country.alpha_2,
                    alpha_3 = pyc.alpha_3,
                    name = country.name,
                    free = country.status == Status.Free
                )

    def delete_countries(apps, schema_editor):
        Country = apps.get_model("api", "Country")
        Country.objects.all().delete()


    operations = [
        migrations.RunPython(load_countries, delete_countries),
    ]