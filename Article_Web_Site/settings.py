from pathlib import Path`r`nimport os
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-unsafe-secret-change-me")
DEBUG = os.environ.get("DEBUG", "1") in ("1","true","True")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "users",
    "articles",
    "category",
    "pages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Article_Web_Site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "category.context_processors.nav_categories"
            ],
        },
    },
]

WSGI_APPLICATION = "Article_Web_Site.wsgi.application"
ASGI_APPLICATION = "Article_Web_Site.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation."
                 "UserAttributeSimilarityValidator")
    },
    {"NAME": ("django.contrib.auth.password_validation."
              "MinimumLengthValidator")},
    {"NAME": ("django.contrib.auth.password_validation."
              "CommonPasswordValidator")},
    {"NAME": ("django.contrib.auth.password_validation."
              "NumericPasswordValidator")},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "users:account"
LOGOUT_REDIRECT_URL = "articles:index"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"     # локально без подтверждения
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

ACCOUNT_LOGIN_METHODS = {"email", "username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]

CSRF_TRUSTED_ORIGINS = ["https://*.ngrok-free.app"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"




