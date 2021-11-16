from django.template.response import SimpleTemplateResponse
from django.utils.timezone import timedelta

from gdpr_helpers.middleware import ConsentExpiredMiddleware
from gdpr_helpers.utils import aware_timedelta_days
from tests.conftest import timezone_now


def test_middleware_process_template_response_not_expired(db, freezer, rf, log):
    fake_request = rf.get("/")
    fake_request.user = log.content_object

    fake_response = SimpleTemplateResponse("", {})

    middleware = ConsentExpiredMiddleware({})
    middleware.process_template_response(fake_request, fake_response)
    assert fake_response.context_data == {}


def test_middleware_process_template_response_expired_by_datetime(db, freezer, rf, log):
    fake_request = rf.get("/")
    fake_request.user = log.content_object

    fake_response = SimpleTemplateResponse("", {})

    move_to = aware_timedelta_days(
        to_move=timezone_now,
        timedelta_days=timedelta(days=+700),
    )
    freezer.move_to(move_to)
    middleware = ConsentExpiredMiddleware({})
    middleware.process_template_response(fake_request, fake_response)
    assert fake_response.context_data == {"consents_expired": True}


def test_middleware_process_template_response_expired_by_change(db, freezer, rf, log):
    fake_request = rf.get("/")
    fake_request.user = log.content_object

    fake_response = SimpleTemplateResponse("", {})
    freezer.move_to(timezone_now + timedelta(seconds=2))
    reason = log.event.all()[0].legal_reason
    reason.flag_text = f"{reason.flag_text}+changed"
    reason.save()

    freezer.move_to(reason.changed_at + timedelta(seconds=1))
    middleware = ConsentExpiredMiddleware({})
    middleware.process_template_response(fake_request, fake_response)
    assert fake_response.context_data == {"consents_expired": True}
