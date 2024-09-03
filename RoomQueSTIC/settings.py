"""
Django settings for hotel_reservation_project project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


"""
This file is part of RoomQueSTIC.

RoomQueSTIC is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RoomQueSTIC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RoomQueSTIC. If not, see <https://www.gnu.org/licenses/>.
"""


import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Charger les variables d'environnement à partir du fichier .env
env_path_django = Path(BASE_DIR) / '.env'
env_path_crestic = Path(BASE_DIR) / '.env.crestic'
load_dotenv(dotenv_path=env_path_crestic)
load_dotenv(dotenv_path=env_path_django)

production_prefix=os.getenv('PRODUCTION_PREFIX')
if production_prefix is None:
    production_prefix=''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$_ag_)$o*q3sein$(q@m_53qiusn&3y_%)j5-ly3!e7cs0dekg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'fullcalendar',

    # 3rd Party
    'crispy_forms',
    'bootstrap_datepicker_plus',

    # Local
    'users.apps.UsersConfig',
    'rooms.apps.RoomsConfig',
    'equipments.apps.EquipmentsConfig',
    'dashboard.apps.DashboardConfig',
    'bookedrooms.apps.BookedroomsConfig',
    'bookedequipments.apps.BookedequipmentsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
]

ROOT_URLCONF = 'RoomQueSTIC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RoomQueSTIC.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + "/" + 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # pour conserver l'authentification par défaut
    'django_cas_ng.backends.CASBackend',  # pour ajouter l'authentification CAS
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CAS_SERVER_URL = f"https://{os.getenv('CAS_HOST')}{os.getenv('CAS_CONTEXT')}/"  # URL du serveur CAS
CAS_PORT = os.getenv('CAS_PORT')
CAS_ROOT_PROXIED_AS = os.getenv('CAS_PROXY')
CAS_VERSION = '2'  # version du protocole CAS, par exemple '3' pour CAS v3.0
LOGIN_URL = f"{os.getenv('CAS_CLIENT_SERVICE_NAME')}/{production_prefix}accounts/login"
CAS_EXTRA_LOGIN_PARAMS = { 'service' : LOGIN_URL }

# LOGIN_URL = 'django_cas_ng.views.login'
# LOGOUT_URL = 'django_cas_ng.views.logout'
CAS_LOGIN_NEXT_PAGE = f'/{production_prefix}'  # URL de redirection après une connexion réussie
# CAS_REDIRECT_URL = f'{production_prefix}'  # URL de redirection après une connexion réussie

CAS_LOGOUT_COMPLETELY = True  # déconnexion complète sur CAS logout
CAS_IGNORE_REFERER = True # ignorer le referer pour éviter les boucles de redirection

CAS_STORE_NEXT = True
CAS_APPLY_ATTRIBUTES_TO_USER = True
CAS_RENAME_ATTRIBUTES = {'mail':'email'}

LOGIN_REQUIRED_IGNORE_VIEW_NAMES = ['cas_ng_login']

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = f'/{production_prefix}static/'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = f'/{production_prefix}media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOM_IMAGE = '/default_room_image/default.jpg'
MEDIA_EQUIPMENT_IMAGE = '/default_equipment_image/default.jpg'

# Configuration de l'envoi d'email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = ''


def get_email_recipients():
    recipients = os.getenv('EMAIL_RECIPIENTS', '')
    return recipients.split(',')


# Charger les destinataires des emails
EMAIL_RECIPIENTS = get_email_recipients()

# Content Security Policy

CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",
]

CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
]

CSP_IMG_SRC = [
    "'self'",
]

CSP_FONT_SRC = [
    "'self'",
]
