# Generated by Django 2.2.19 on 2021-03-15 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdpr_helpers', '0007_populate_slug_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legalreason',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='Slug del consenso'),
            preserve_default=False,
        ),
    ]
