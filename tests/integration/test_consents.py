from django.urls import reverse
from django.utils.timezone import timedelta

from gdpr_helpers.models import PrivacyLog
from gdpr_helpers.utils import aware_timedelta_days
from tests.conftest import timezone_now


def test_user_set_consents_at_registration(
    db, client, freezer, django_user_model, registration_legal_reason_group
):
    start = timezone_now + timedelta(seconds=1)
    freezer.move_to(start)

    # Create a user with correct consents
    data = {
        "username": "Megatron",
        "password": "transformandriseup",
        "privacy_registration": True,
        "privacy_marketing": False,
    }
    url = reverse("dummy-registration")
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    user = django_user_model.objects.get(username="Megatron")

    # Check privacy log is correct before expiration
    move_to = start + timedelta(seconds=1)
    freezer.move_to(move_to)
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    assert log.event.get(legal_reason__slug="registration").accepted is True
    assert log.event.get(legal_reason__slug="marketing").accepted is False
    assert log.is_expired is False


def test_middleware(db, client, freezer, log):
    """Testing middleware"""
    user = log.content_object

    url = reverse("dummy-registration")
    client.force_login(user)

    # No expiration
    start = timezone_now + timedelta(seconds=2)
    freezer.move_to(start)
    response = client.get(url)
    assert response.status_code == 200
    # Check context modified by middleware
    assert response.context_data.get("consents_expired", None) is None
    # Check log expiration
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    registration = log.event.get(legal_reason__slug="registration")
    marketing = log.event.get(legal_reason__slug="marketing")
    assert registration.legal_reason.check_expiration(log.created) is False
    assert registration.accepted is True
    assert marketing.legal_reason.check_expiration(log.created) is False
    assert marketing.accepted is False

    # Change Marketing flag
    move_to = start + timedelta(seconds=1)
    freezer.move_to(move_to)
    legal_reason = log.event.get(legal_reason__slug="marketing").legal_reason
    legal_reason.flag_text += "changed"
    legal_reason.save()

    response = client.get(url)
    assert response.status_code == 200
    # Check context modified by middleware
    assert response.context_data.get("consents_expired", None) is True
    # Check log expiration
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    registration = log.event.get(legal_reason__slug="registration")
    marketing = log.event.get(legal_reason__slug="marketing")
    assert registration.legal_reason.check_expiration(log.created) is False
    assert registration.accepted is True
    assert marketing.legal_reason.check_expiration(log.created) is True
    assert marketing.accepted is False

    # Move into the future!
    move_to = aware_timedelta_days(to_move=move_to, timedelta_days=timedelta(days=+365))
    freezer.move_to(move_to)

    assert response.status_code == 200
    # Check context modified by middleware
    assert response.context_data.get("consents_expired", None) is True
    # Check log expiration
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    registration = log.event.get(legal_reason__slug="registration")
    marketing = log.event.get(legal_reason__slug="marketing")
    assert registration.legal_reason.check_expiration(log.created) is True
    assert registration.accepted is True
    assert marketing.legal_reason.check_expiration(log.created) is True
    assert marketing.accepted is False
