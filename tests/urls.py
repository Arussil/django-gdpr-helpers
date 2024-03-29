from django.urls import path
from django.views.generic import TemplateView

from tests.views import DummyRegistrationView, DummyRenewConsentsView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="tests/template.html"),
        name="dummy-homepage",
    ),
    path("registation", DummyRegistrationView.as_view(), name="dummy-registration"),
    path("renew", DummyRenewConsentsView.as_view(), name="dummy-renew-consents"),
]
