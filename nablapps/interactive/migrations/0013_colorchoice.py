# Generated by Django 2.1.13 on 2019-11-07 20:36

import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("interactive", "0012_remove_empty_quizreplies"),
    ]

    operations = [
        migrations.CreateModel(
            name="ColorChoice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile(
                                    "(^#[a-f0-9]{3,6}$)|(^rgb\\s*\\(\\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\\s*,\\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\\s*)\\))|(^hsl\\s*\\(\\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\\s*,\\s*(100%|[0-9]{1,2}%)\\s*,\\s*(100%|[0-9]{1,2}%)\\s*\\)$)",
                                    2,
                                ),
                                "Enter a valid color in CSS format.",
                                "invalid",
                            )
                        ],
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
