# Generated by Django 3.2.22 on 2024-01-08 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailFeed",
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
                (
                    "created",
                    models.DateTimeField(auto_created=True, verbose_name="Opprettet"),
                ),
                ("name", models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
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
                (
                    "created",
                    models.DateTimeField(auto_created=True, verbose_name="Opprettet"),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "mailfeed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailfeed.mailfeed",
                    ),
                ),
            ],
        ),
    ]
