# Django settings for sandbox project.
import os

PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "db.sqlite3"),
    }
}

USE_TZ = True

TIME_ZONE = "Europe/London"

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, "locale"),)


MEDIA_ROOT = ""

MEDIA_URL = ""

STATIC_ROOT = ""

STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

SECRET_KEY = "TEST_NOT_SO_SECRET_KEY"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "gdpr_helpers.middleware.ConsentExpiredMiddleware",
)

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "tests",
    "gdpr_helpers",
)
