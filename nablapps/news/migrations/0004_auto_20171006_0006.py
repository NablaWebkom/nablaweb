# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0003_auto_20171005_2335"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="headline",
            field=models.CharField(blank=True, max_length=100, verbose_name="tittel"),
        ),
    ]
