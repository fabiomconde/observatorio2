"""
Django settings for the Observatório Socioambiental project.

Production-ready defaults via env vars. Safe to develop locally with DEBUG=True.
"""

import os
from pathlib import Path
from decouple import config

# -------------------------------------------------------------------- #
# Paths
# -------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------------------------- #
# Security
# -------------------------------------------------------------------- #
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-CHANGE-ME-in-production-#9f8a7b6c5d4e3f2a1b0c",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "https://observatorio.provaconceito.tech,http://observatorio.provaconceito.tech,http://127.0.0.1:8000,http://localhost:8000",
    ).split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



# -------------------------------------------------------------------- #
# Applications
# -------------------------------------------------------------------- #
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # for `intcomma`, `naturaltime` in templates
    "django_user_agents",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# -------------------------------------------------------------------- #
# Database
# -------------------------------------------------------------------- #
DB_ENGINE = os.environ.get("DB_ENGINE", "postgres")

if DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="observatorio_db"),
            "USER": config("DB_USER", default="app_observatorio_user"),
            "PASSWORD": config("DB_PASSWORD", default="Qwe135@@a"),
            "HOST": config("DB_HOST", default="meubanco_postgres"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    SQLITE_DIR = BASE_DIR / "sqlite_data"
    SQLITE_DIR.mkdir(parents=True, exist_ok=True)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            # Salva o banco dentro de uma pasta segura chamada 'sqlite_data'
            "NAME": SQLITE_DIR / "db.sqlite3",
        }
    }


# -------------------------------------------------------------------- #
# Password validation
# -------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------------------------------------------------------- #
# Internationalization
# -------------------------------------------------------------------- #
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------- #
# Static / Media files
# -------------------------------------------------------------------- #
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -------------------------------------------------------------------- #
# Default PK
# -------------------------------------------------------------------- #
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -------------------------------------------------------------------- #
# Project-specific configuration
# -------------------------------------------------------------------- #
# Used in templates via {{ SITE_NAME }}, etc.
from django.conf import settings  # noqa: E402  (keep at bottom)

SITE_NAME = "Observatório de Conflitos Socioambientais e Direitos Humanos"
SITE_TAGLINE = "Ciência aberta, tecnologia e impacto para políticas públicas."
SITE_DESCRIPTION = (
    "Iniciativa de pesquisa, formação engajada e incidência política sobre os conflitos socioambientais e as condições de acesso aos direitos humanos em Porto Velho."
)

# Paleta inspirada em observatórios institucionais
SITE_THEME = {
    "primary": "#0d3b66",     # azul institucional
    "primary_dark": "#082a4a",
    "primary_light": "#1d4e89",
    "accent": "#ee964b",      # laranja/dourado para CTAs e destaques
    "success": "#1d7a47",
    "muted": "#5a6678",
    "bg": "#f4f6f8",
}
