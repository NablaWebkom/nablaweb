# Generated by Django 3.2.22 on 2024-01-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailfeed',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Opprettet'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Opprettet'),
        ),
    ]
