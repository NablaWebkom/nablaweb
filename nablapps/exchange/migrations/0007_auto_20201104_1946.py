# Generated by Django 3.0.7 on 2020-11-04 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0006_merge_20201023_1226"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="Navn på faget", max_length=50)),
                ("code", models.CharField(help_text="Fagkode", max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name="exchange",
            name="fag",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subject_set",
                to="exchange.Subject",
            ),
        ),
    ]
