from gdpr_helpers.models import PrivacyLog
from tests.conftest import timezone_now


def test_get_privacy_logs_for_object(
    registration_legal_reason_group, registered_user, db
):
    log_created = PrivacyLog.objects.create_log(
        content_object=registered_user,
        cleaned_data={"privacy_registration": True, "privacy_marketing": True},
    )
    log = PrivacyLog.objects.get_privacy_logs_for_object(registered_user)
    assert log_created == log


def test_get_consents_for_object(
    registration_legal_reason_group, registered_user, db, freezer
):
    freezer.move_to(timezone_now)
    expected = [
        {"slug": "registration", "accepted": True, "given_at": timezone_now},
        {"slug": "marketing", "accepted": False, "given_at": timezone_now},
    ]
    PrivacyLog.objects.create_log(
        content_object=registered_user,
        cleaned_data={"privacy_registration": True, "privacy_marketing": False},
    )
    assert PrivacyLog.objects.get_consents_for_object(registered_user) == expected
