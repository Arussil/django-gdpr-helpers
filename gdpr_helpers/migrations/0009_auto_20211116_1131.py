# Generated by Django 2.2.19 on 2021-11-16 11:31

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gdpr_helpers", "0008_remove_slug_null"),
    ]

    operations = [
        migrations.AddField(
            model_name="legalreason",
            name="changed_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Data modifica"),
        ),
        migrations.AddField(
            model_name="legalreason",
            name="duration",
            field=models.DurationField(
                default=datetime.timedelta(days=365), verbose_name="Durata"
            ),
        ),
        migrations.AddField(
            model_name="legalreasongroup",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Attivo"),
        ),
        migrations.AddField(
            model_name="legalreasongroup",
            name="is_renewable",
            field=models.BooleanField(default=False, verbose_name="Rinnovabile"),
        ),
    ]
