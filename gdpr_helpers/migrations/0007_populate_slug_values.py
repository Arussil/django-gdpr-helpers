# Generated by Django 2.2.19 on 2021-03-15 10:20

from django.db import migrations

def populate_slugs(apps, schema_editor):
    LegalReason = apps.get_model("gdpr_helpers", "LegalReason")
    for legal_reason in LegalReason.objects.all():
        legal_reason.slug = f"{legal_reason.pk}"
        legal_reason.save(update_fields=["slug"])

class Migration(migrations.Migration):

    dependencies = [
        ('gdpr_helpers', '0006_add_slug_field'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_code=migrations.RunPython.noop)
    ]