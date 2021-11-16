from django.views.generic import FormView

from tests.forms import DummyForm, DummyRenewForm


class DummyRegistrationView(FormView):
    template_name = "tests/template.html"
    form_class = DummyForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class DummyRenewConsentsView(FormView):
    template_name = "tests/template.html"
    form_class = DummyRenewForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
