from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from .utils import form_registry


class GdprHelpersConfig(AppConfig):
    name = "gdpr_helpers"
    verbose_name = _("Gdpr helpers")

    def ready(self):
        """Autodiscover for form registry"""
        form_registry.autodiscover()
