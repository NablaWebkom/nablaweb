# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_remove_news_allow_comments"),
    ]

    operations = [
        migrations.RemoveField(model_name="news", name="priority",),
        migrations.AlterField(
            model_name="news",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
