from tests.forms import DummyForm, DummyChangeForm, DummyRenewForm
from gdpr_helpers.utils import form_registry

def test_form_registry():
    assert set(form_registry.registry) == set(["tests.forms.DummyForm", "tests.forms.DummyChangeForm", "tests.forms.DummyRenewForm"])
