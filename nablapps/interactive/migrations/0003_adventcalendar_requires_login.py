# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-31 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0002_auto_20171106_2322"),
    ]

    operations = [
        migrations.AddField(
            model_name="adventcalendar",
            name="requires_login",
            field=models.BooleanField(
                default=False, verbose_name="Krever innlogging for å se side"
            ),
        ),
    ]
