"""
Django settings for thomasd9e project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path

from .utils import download_service_account_key
from google.oauth2.service_account import Credentials

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_PATH = os.getenv("SECRET_PATH")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = [
    "thomasd9e.com",
    "www.thomasd9e.com",
    "127.0.0.1",
    "thomasd9e.uc.r.appspot.com",
]

SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    "blog",
    "ckeditor",
    "ckeditor_uploader",
    "storages",
    "sslserver",
    "accounts",
    "website",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "thomasd9e.middleware.SecureMiddleware",
]

ROOT_URLCONF = "thomasd9e.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "thomasd9e.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Check if the app is deployed or running locally
DEPLOYED = os.getenv("DEPLOYED", "False") == "True"

if DEPLOYED:
    # Use the instance connection name for the deployed app
    DB_HOST = os.getenv("CLOUD_HOST")
else:
    # Use the Public IP for local development
    DB_HOST = os.getenv("DB_HOST")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": DB_HOST,
        "PORT": os.getenv("DB_PORT"),
    }
}

# Email
# https://docs.djangoproject.com/en/4.1/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


AUTH_USER_MODEL = "accounts.CustomUser"  # Assuming you'll have an 'accounts' app with a custom user model.

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "thomasd9e.backends.CaseInsensitiveEmailBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

GS_BUCKET_NAME = "thomasd9e.appspot.com"
GS_PROJECT_ID = "thomasd9e"
# Load the credentials from the downloaded key
GS_CREDENTIALS = Credentials.from_service_account_file(download_service_account_key())

# Static file configuration
STATIC_URL = "https://storage.googleapis.com/{}/static/".format(GS_BUCKET_NAME)
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

# Media file configuration
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
MEDIA_URL = "https://storage.googleapis.com/{}/media/".format(GS_BUCKET_NAME)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "website", "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

CKEDITOR_BASEPATH = "https://storage.googleapis.com/thomasd9e.appspot.com/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
