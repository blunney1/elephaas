import os
import sys
import ldap
import logging

from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

"""
Django settings for pg_admin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']


# Application definition

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'db_user',
    'db_instance',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pg_admin.urls'
WSGI_APPLICATION = 'pg_admin.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# See local_settings.py

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# LDAP-specific settings. Set DN and PASSWORD in local_settings.py.

AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

AUTH_LDAP_SERVER_URI = "ldap://chicagodc.peak6.net"
AUTH_LDAP_REQUIRE_GROUP = "cn=Infrastructure,OU=Shared Services,OU=Distribution Groups,OU=Groups,DC=peak6,DC=net"

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: False,
    ldap.OPT_X_TLS_DEMAND: True,
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
}

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300

AUTH_LDAP_START_TLS = True

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Technology,ou=Shared Services,ou=User Accounts,dc=peak6,dc=net",
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)')

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": AUTH_LDAP_REQUIRE_GROUP,
    "is_staff": AUTH_LDAP_REQUIRE_GROUP,
    "is_superuser": AUTH_LDAP_REQUIRE_GROUP
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=peak6,dc=net",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

# There are some settings that should not be saved to source control. Those
# settings are in the local settings file, and this application will not run
# without them. These are things like database connection settings, secret
# keys, and LDAP authentication.

try:
  from local_settings import *
except ImportError:
  print "Could not import local settings!"
  sys.exit()

# Now that the local setting import is done, override the NULL display.
# The Django default of (none) is pretty irritating.

from django.contrib.admin.views import main
main.EMPTY_CHANGELIST_VALUE = '-'