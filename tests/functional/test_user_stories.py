from django.urls import reverse
from django.utils.timezone import timedelta

from gdpr_helpers.models import PrivacyLog
from gdpr_helpers.utils import aware_timedelta_days
from tests.conftest import timezone_now


def test_user_consent_registration_expiration_and_renew(
    db, client, freezer, django_user_model, registration_legal_reason_group
):
    """
    As an user i want to register to a site so i can use it services.
    As an user i want to give consent to data processing so my rights are respected.
    """
    registration_url = reverse("dummy-registration")
    renew_url = reverse("dummy-renew-consents")
    homepage_url = reverse("dummy-homepage")
    start = timezone_now + timedelta(seconds=1)
    freezer.move_to(start)
    # Register user with consents
    data = {
        "username": "Megatron",
        "password": "transformandriseup",
        "privacy_registration": True,
        "privacy_marketing": False,
    }
    response = client.post(registration_url, data)
    assert django_user_model.objects.count() == 1
    assert PrivacyLog.objects.count() == 1

    user = django_user_model.objects.get(username="Megatron")
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    assert log.is_expired is False

    move_to = start + timedelta(seconds=1)
    freezer.move_to(move_to)
    # Changing a flag makes the log expire and the user can give new consents
    # the middleware set a flag on context_data so we can offer user a way to renew consents
    legal_reason = log.event.get(legal_reason__slug="marketing").legal_reason
    legal_reason.flag_text += "changed"
    legal_reason.save()

    # User visit again and the middleware check consents expiration
    move_to = move_to + timedelta(seconds=1)
    client.force_login(user)
    response = client.get(homepage_url)
    assert response.context_data.get("consents_expired", None) is True
    # User now give new consents
    data = {
        "privacy_registration": True,
        "privacy_marketing": True,
    }
    response = client.post(renew_url, data, follow=True)

    assert response.context_data.get("consents_expired", None) is None
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    assert log.is_expired is False
    assert log.event.get(legal_reason__slug="registration").accepted is True
    assert log.event.get(legal_reason__slug="marketing").accepted is True

    # User visits after the registration consents is expired
    move_to = aware_timedelta_days(to_move=move_to, timedelta_days=timedelta(days=+365))
    freezer.move_to(move_to)
    client.force_login(user)
    response = client.get(homepage_url)
    assert response.context_data.get("consents_expired", None) is True

    # User now give new consents
    data = {
        "privacy_registration": True,
        "privacy_marketing": False,
    }
    response = client.post(renew_url, data, follow=True)
    assert response.context_data.get("consents_expired", None) is None
    log = PrivacyLog.objects.get_privacy_logs_for_object(user)
    assert log.is_expired is False
    assert log.event.get(legal_reason__slug="registration").accepted is True
    assert log.event.get(legal_reason__slug="marketing").accepted is False
