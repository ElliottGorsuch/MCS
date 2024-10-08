# Generated by Django 5.1.1 on 2024-09-24 19:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mountain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("elevation", models.FloatField()),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("distance", models.FloatField()),
                ("elevation_gain", models.FloatField()),
                ("environment", models.CharField(max_length=100)),
                ("technical_difficulty", models.CharField(max_length=100)),
                ("glacier_travel", models.CharField(max_length=100)),
                ("danger_factors", models.TextField()),
                ("duration", models.FloatField()),
                ("permit_required", models.CharField(max_length=10)),
                ("permit_cost_over_24", models.FloatField()),
                ("permit_cost_under_24", models.FloatField()),
                ("access_difficulty", models.CharField(max_length=100)),
                ("gear_required", models.TextField()),
                (
                    "mountain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="routes",
                        to="climbs.mountain",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.CharField(max_length=20)),
                ("weather_conditions", models.TextField()),
                ("avalanche_risk", models.CharField(max_length=20)),
                (
                    "route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather_data",
                        to="climbs.route",
                    ),
                ),
            ],
        ),
    ]
