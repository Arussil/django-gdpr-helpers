from django import forms
from django.contrib.auth import get_user_model

from gdpr_helpers.forms import GDPRFormMixin
from gdpr_helpers.models import PrivacyLog


class DummyForm(GDPRFormMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        where = "registration"
        fields = (
            "username",
            "password",
        )

    def save(self):
        user = super().save()
        PrivacyLog.objects.create_log(
            content_object=user, cleaned_data=self.cleaned_data
        )
        return user


class DummyRenewForm(GDPRFormMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        where = "registration"

    def save(self):
        PrivacyLog.objects.create_log(
            content_object=self.user, cleaned_data=self.cleaned_data
        )
