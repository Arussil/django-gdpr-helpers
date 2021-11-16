import pytest
from django import forms

from gdpr_helpers.models import PrivacyEvent, PrivacyLog
from tests.forms import DummyForm


def test_legal_reason_group_as_form_fields(registration_legal_reason_group):
    form_fields = registration_legal_reason_group.get_as_form_fields()
    assert len(form_fields) == 2
    assert form_fields[0]["field_name"] == "privacy_registration"
    assert isinstance(form_fields[0]["field"], forms.BooleanField)
    assert form_fields[1]["field_name"] == "privacy_marketing"
    assert isinstance(form_fields[1]["field"], forms.TypedChoiceField)


def test_form_has_legal_reason_group_fields(registration_legal_reason_group):
    form = DummyForm()
    assert "privacy_registration" in form.fields
    assert "privacy_marketing" in form.fields
    assert "privacy_profiling" not in form.fields


@pytest.mark.parametrize(
    "privacy_registration, privacy_registration_valid", [(True, True), (False, False)]
)
@pytest.mark.parametrize(
    "privacy_marketing, privacy_marketing_valid", [(True, True), (False, True)]
)
def test_form_is_valid(
    registration_legal_reason_group,
    privacy_registration,
    privacy_marketing,
    privacy_registration_valid,
    privacy_marketing_valid,
):
    form = DummyForm(
        {
            "username": "Megatron",
            "password": "transformandriseup",
            "privacy_registration": privacy_registration,
            "privacy_marketing": privacy_marketing,
        }
    )
    assert form.is_valid() == all([privacy_registration_valid, privacy_marketing_valid])


def test_form_works_without_legal_reasons(db):
    form = DummyForm({"username": "Megatron", "password": "trasformandriseup"})
    assert "privacy_registration" not in form.fields
    assert "privacy_marketing" not in form.fields
    assert form.is_valid() is True


def test_log_is_generated(registration_legal_reason_group, registered_user, db):
    PrivacyLog.objects.create_log(
        content_object=registered_user,
        cleaned_data={"privacy_registration": True, "privacy_marketing": True},
    )
    assert PrivacyLog.objects.count() == 1
    assert PrivacyEvent.objects.count() == 2


def test_log_are_correct(log):
    event_1 = PrivacyEvent.objects.get(
        privacy_log=log, legal_reason__slug="registration"
    )
    event_2 = PrivacyEvent.objects.get(privacy_log=log, legal_reason__slug="marketing")
    assert event_1.accepted is True
    assert event_2.accepted is False
