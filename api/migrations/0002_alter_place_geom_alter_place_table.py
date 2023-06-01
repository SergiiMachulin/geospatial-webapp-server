# Generated by Django 4.2.1 on 2023-05-30 10:47

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="geom",
            field=django.contrib.gis.db.models.fields.PointField(
                db_index=True, srid=4326
            ),
        ),
        migrations.AlterModelTable(
            name="place",
            table="places",
        ),
    ]
