# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-02 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("poll", "0007_poll_content_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="poll",
            name="content_type",
        ),
    ]
