# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-18 15:16
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interactive", "0006_auto_20181122_1957"),
    ]

    operations = [
        migrations.RemoveField(model_name="result", name="length",),
        migrations.AddField(
            model_name="result", name="solution", field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="codetask", name="task", field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="result",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="interactive.CodeTask"
            ),
        ),
        migrations.AlterField(
            model_name="result",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
