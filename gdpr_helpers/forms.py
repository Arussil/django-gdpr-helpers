from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LegalReasonGroup, PrivacyLog
from .utils import form_registry, get_class_import_path

class GDPRFormMixin():
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        form_registry.register(cls)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            group = LegalReasonGroup.objects.get(connected_to__icontains=get_class_import_path(self.__class__))
        except LegalReasonGroup.DoesNotExist:
            pass
        else:
            for reason in group.get_as_form_fields():
                self.fields[reason["field_name"]] = reason["field"]


class LegalReasonGroupForm(forms.ModelForm):
    connected_to = forms.MultipleChoiceField(
        label=_("Form collegato"),
        choices=form_registry.choices
    )
    class Meta:
        model = LegalReasonGroup
        fields = [
            "connected_to",
            "is_active",
            "is_renewable",
        ]
