# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 13:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0013_auto_20171017_0144"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newsarticle",
            name="view_counter",
        ),
    ]
