# Generated by Django 3.0.7 on 2020-11-04 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0008_auto_20201104_2016"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="code",
            field=models.CharField(max_length=50, verbose_name="Emnekode"),
        ),
        migrations.AlterField(
            model_name="subject",
            name="exchange",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="exchange.Exchange"
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Emnenavn"),
        ),
    ]
