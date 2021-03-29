# Generated by Django 2.2.19 on 2021-03-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdpr_helpers', '0005_legalreason_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalreason',
            name='name',
        ),
        migrations.AddField(
            model_name='legalreason',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug del consenso'),
        ),
    ]