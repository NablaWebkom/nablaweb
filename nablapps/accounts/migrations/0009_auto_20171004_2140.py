# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 21:40
from __future__ import unicode_literals

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0008_nablagroup_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nablauser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]
