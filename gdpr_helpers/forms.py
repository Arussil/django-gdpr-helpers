from .models import LegalReasonGroup, PrivacyLog


class GDPRFormMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            group = LegalReasonGroup.objects.get(where=self.Meta.where)
            for reason in group.get_as_form_fields():
                self.fields[reason["field_name"]] = reason["field"]
        except LegalReasonGroup.DoesNotExist:
            pass
