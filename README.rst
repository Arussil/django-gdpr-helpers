.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
======
GDPR Helpers
======

GDPR Helpers is a Django app for easy GDPR compliance.

Quickstart
-------

Install Django GDPR Helpers:
   pip install -e git+git@github.com:Arussil/django-gdpr-helpers.git

Add it to your `INSTALLED_APPS`:

.. code-block:: python
   INSTALLED_APPS = (
      ...
      'gdpr_helpers',
      ...
   )

Define your reasons for asking personal data and assign them to a group:

.. code-block:: python

   from gdpr_helpers.models import LegalReasonGroup, LegalReason

   legal_group = LegalReasonGroup.objects.create(where="registration")

   LegalReason.objects.create(legal_group=legal_group, flag_text="Required for registration", slug="registration", active=True, required=True)
   LegalReason.objects.create(legal_group=legal_group, flag_text="Optional for registration", slug="marketing", active=True, required=False)

Or use the django-admin.

Add the Mixin to a form that create an object and need privacy flags, remember to save the PrivacyLog in someplace:

.. code-block:: python

   from django import forms
   from gdpr_helpers.forms import GDPRFormMixin
   from .models import User


   class RegistrationForm(GDPRFormMixin):
      class Meta:
        model = User
        where = "registration"
        fields = ("whatever_fields_from_model",)

      def save(self):
        user = super().save()
        PrivacyLog.objects.create_log(content_object=user, cleaned_data=self.cleaned_data)
        return user

Note that the privacy fields are already injected in the form.

Filling the form will now create logs for the object created.

Features
--------

* Can define Legal reason for which you are collecting personal data
* Create logs for the data you collected with a timestamp and what the user consented to
* Logs are anonymous

TODO
----

* When the user/system/admin removes the object we must keep a reference, maybe an unique ID that binds the deleted record to the logs
* Adding a serializer to use it on rest_framework project
* Add the ability to define a timer for data based on Legal reason, so we can destroy it after it expires or ask the user for another consent
