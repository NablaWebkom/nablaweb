# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-28 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("poll", "0001_squashed_0008_remove_poll_content_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="answer",
            field=models.CharField(
                blank=True, default="", max_length=1000, verbose_name="Svar"
            ),
        ),
    ]
