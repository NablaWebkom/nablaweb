# Generated by Django 3.1.14 on 2022-09-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_auto_20210413_1346"),
    ]

    operations = [
        migrations.AddField(
            model_name="nablauser",
            name="darkmode",
            field=models.BooleanField(default=False, verbose_name="darkmode"),
        ),
    ]
