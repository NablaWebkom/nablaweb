# Generated by Django 2.1.9 on 2019-10-03 22:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import image_cropping.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exchange", "0002_auto_20161213_1451"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeNewsArticle",
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
                    "picture",
                    models.ImageField(
                        blank=True,
                        help_text="Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.",
                        null=True,
                        upload_to="uploads/news_pictures",
                        verbose_name="Bilde",
                    ),
                ),
                (
                    "cropping",
                    image_cropping.fields.ImageRatioField(
                        "picture",
                        "770x300",
                        adapt_rotation=False,
                        allow_fullsize=False,
                        free_crop=False,
                        help_text=None,
                        hide_image_field=False,
                        size_warning=False,
                        verbose_name="Beskjæring",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Publiseringsdato"
                    ),
                ),
                (
                    "last_changed_date",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Redigeringsdato"
                    ),
                ),
                (
                    "headline",
                    models.CharField(blank=True, max_length=100, verbose_name="tittel"),
                ),
                (
                    "lead_paragraph",
                    models.TextField(
                        blank=True,
                        help_text="Vises på forsiden og i artikkelen",
                        verbose_name="ingress",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        blank=True,
                        help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.',
                        verbose_name="brødtekst",
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchangenewsarticle_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Opprettet av",
                    ),
                ),
                (
                    "last_changed_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchangenewsarticle_edited",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Endret av",
                    ),
                ),
            ],
            options={
                "verbose_name": "Nyhetsartikkel",
                "verbose_name_plural": "Nyhetsartikler",
                "abstract": False,
            },
        ),
    ]
