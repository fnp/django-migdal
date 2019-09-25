"""
Django settings for core project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')1^j9pxlee5bz+$-g1_tphmnip=u^78r+xskny()61)ulk7n4w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites', # Used by django_comments.
    'django_comments', # Used by migdal.
    'django_comments_xtd', # Used by migdal.
    'migdal',
    'fnpdjango', # Has template tags used in default migdal templates.
    'sorl.thumbnail', # Has template tags used in default migdal templates.
    'fnp_django_pagination', # Has template tags used in default migdal templates.
    'django_gravatar', # Has template tags used in default migdal templates.
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',  # Needed to set language.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fnp_django_pagination.middleware.PaginationMiddleware', # Used in default migdal templates.
)

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# We have to provide a base template.
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'core/templates'),
]
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request", # Used in template tags.
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': TEMPLATE_DIRS,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.request", # Used in template tags.
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            ],
        }
    }
]


# These match languages in migrations.
LANGUAGE_CODE = 'pl'
LANGUAGES = [
        ('pl', 'Polish'),
        ('en', 'English'),
        ]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


# Match default migdal markup type.
from fnpdjango.utils.text.textilepl import textile_pl
MARKUP_FIELD_TYPES = (
    ('textile_pl', textile_pl),
)


# Create an Entry type.
from fnpdjango.utils.settings import LazyUGettextLazy as gettext
from migdal.helpers import EntryType

MIGDAL_TYPES = (
    EntryType('blog', gettext('blog'), commentable=True, on_main=True),
    EntryType('info', gettext('info'), commentable=False, on_main=False),
)


# Needed for Haystack to work.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/prawokultury'
    },
}

# django_comments need SITE_ID.
SITE_ID = 1
