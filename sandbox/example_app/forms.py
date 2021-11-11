from django import forms
from gdpr_helpers.forms import GDPRFormMixin
from gdpr_helpers.models import PrivacyLog

from .models import ExampleModel


class ExampleForm(GDPRFormMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        where = "contact_form"
        exclude = ()

    def save(self):
        saved_object = super().save()
        PrivacyLog.objects.create_log(
            content_object=saved_object,
            cleaned_data=self.cleaned_data
        )
        return saved_object
