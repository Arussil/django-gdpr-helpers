from django.utils.timezone import timedelta
from model_bakery import baker

from gdpr_helpers.utils import aware_timedelta_days


def test_legal_reason_check_expiration_by_date(db, freezer):
    """Consent expired by date and time"""
    legal_reason = baker.make("gdpr_helpers.LegalReason", duration=timedelta(days=2))
    event = baker.make("gdpr_helpers.PrivacyEvent", legal_reason=legal_reason)

    assert legal_reason.check_expiration(event.privacy_log.created) is False
    move_to = aware_timedelta_days(
        to_move=event.privacy_log.created,
        timedelta_days=timedelta(days=+2),
    )
    freezer.move_to(move_to + timedelta(seconds=+1))
    assert legal_reason.check_expiration(event.privacy_log.created) is True


def test_legal_reason_check_expiration_by_change(db, freezer):
    """Consent expired by LegalReasonChange"""
    legal_reason = baker.make("gdpr_helpers.LegalReason", duration=timedelta(days=365))
    event = baker.make("gdpr_helpers.PrivacyEvent", legal_reason=legal_reason)

    assert legal_reason.check_expiration(event.privacy_log.created) is False
    freezer.move_to(event.privacy_log.created + timedelta(seconds=+1))
    legal_reason.flag_text = f"{legal_reason.flag_text}+changed"
    legal_reason.save()
    assert legal_reason.check_expiration(event.privacy_log.created) is True
