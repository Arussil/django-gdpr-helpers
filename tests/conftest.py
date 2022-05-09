import pytest
from django.utils.timezone import now, timedelta
from model_bakery import baker

from gdpr_helpers.models import LegalReason, LegalReasonGroup, PrivacyLog

timezone_now = now()


@pytest.fixture
def registration_legal_reason_group(db, freezer) -> LegalReasonGroup:
    freezer.move_to(timezone_now)
    group = LegalReasonGroup.objects.create(
        connected_to=["tests.forms.DummyForm", "tests.forms.DummyRenewForm, DummyChangeForm"], 
        is_renewable=True
    )
    LegalReason.objects.create(
        legal_group=group,
        required=True,
        active=True,
        flag_text="Required for registration",
        slug="registration",
    )
    LegalReason.objects.create(
        legal_group=group,
        required=False,
        active=True,
        flag_text="Optional for registration",
        slug="marketing",
    )
    LegalReason.objects.create(
        legal_group=group,
        required=False,
        flag_text="Required for registration, but not active",
        slug="profiling",
    )
    return group


@pytest.fixture
def registered_user(db, django_user_model, freezer):
    freezer.move_to(timezone_now + timedelta(seconds=1))
    return baker.make(
        django_user_model, username="Megatron", password="transformandriseup"
    )


@pytest.fixture
def log(db, registration_legal_reason_group, registered_user, freezer) -> PrivacyLog:
    """Created 1 second after the LegalReason"""
    freezer.move_to(timezone_now + timedelta(seconds=1))
    cleaned_data = {"privacy_registration": True, "privacy_marketing": False}
    return PrivacyLog.objects.create_log(
        content_object=registered_user, cleaned_data=cleaned_data
    )
