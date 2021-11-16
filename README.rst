.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

============
GDPR Helpers
============

GDPR Helpers is a Django app for easy GDPR compliance.

Quickstart
==========

Install Django GDPR Helpers:
   pip install django-gdpr-helpers

Add it to your `INSTALLED_APPS`:

.. code-block:: python

   INSTALLED_APPS = (
      ...
      'gdpr_helpers',
      ...
   )

Define your reasons for asking personal data and assign them to a group:

.. code-block:: python

   from gdpr_helpers.models import LegalReasonGroup, egalReason

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
========

* Can define Legal reason for which you are collecting personal data
* Can define duration for the consents
* Create logs for the data you collected with a timestamp and what the user consented to
* Logs are anonymous

Changelog
=========

Version 0.5.0
-------------

models.PrivacyLog
~~~~~~~~~~~~~~~~~
- New property is_expired: if anyof the LegalReason are expired return True.

models.LegalReasonGroup
~~~~~~~~~~~~~~~~~~~~~~~
- New field "is_nenewable": flag the log as renewable (duh), default to False.

models.LegalReason
~~~~~~~~~~~~~~~~~~
- New field "duration": as we can't have user consents for data processing for an indefinite period this will store how log we can use the data for this purpose, default to 365 days.
- New field "changed_at": this is a Django auto_now field, when a LegalReason change then we must expire the corresponding log.
- New method check_expiration: return True if the consents is expired or the LegalReason is changed

middleware.ConsentExpiredMiddleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- A middleware that check PrivacyLog for a user instance (so the consents given during registration) and add some context to response if True. This is mostly as an example of how to handle consents expiration, but it can be used.
