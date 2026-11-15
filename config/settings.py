"""
Django settings for the Observatório Socioambiental project.
Configuração híbrida automática: Dev Local vs. Produção (Docker / VPS).
"""
import importlib.util
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv_file(dotenv_path: Path) -> dict:
    """Lê variáveis do arquivo .env sem depender de pacotes externos."""
    env_vars = {}
    if not dotenv_path.exists():
        return env_vars
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


_DOTENV = _load_dotenv_file(BASE_DIR / ".env")


def get_env(key: str, default: str = "") -> str:
    """Prioriza variável de ambiente do sistema/container, depois .env, depois default."""
    return os.environ.get(key, _DOTENV.get(key, default))


# ==============================================================================
# DETECÇÃO HÍBRIDA DE AMBIENTE (DEV LOCAL vs. PRODUÇÃO DOCKER/VPS)
# ==============================================================================
IN_DOCKER = os.path.exists("/.dockerenv")
ENVIRONMENT = get_env("ENVIRONMENT", "prod" if IN_DOCKER else "dev").lower()
IS_PROD = IN_DOCKER or ENVIRONMENT in ("prod", "production")

SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-CHANGE-ME-in-production-#9f8a7b6c5d4e3f2a1b0c",
)

if IS_PROD:
    DEBUG = get_env("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")
    _hosts_env = get_env(
        "DJANGO_ALLOWED_HOSTS",
        "observatorio.provaconceito.tech,observapvh,127.0.0.1,localhost",
    )
    ALLOWED_HOSTS = [h.strip() for h in _hosts_env.split(",") if h.strip()]

    _csrf_env = get_env(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "https://observatorio.provaconceito.tech,http://observatorio.provaconceito.tech",
    )
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_env.split(",") if o.strip()]

    # Banco de Dados PostgreSQL (Rede Docker na VPS)
    DB_NAME = get_env("DB_NAME", "observatorio_db")
    DB_USER = get_env("DB_USER", "app_observatorio_user")
    DB_PASSWORD = get_env("DB_PASSWORD", "Qwe135@@a")
    DB_HOST = get_env("DB_HOST", "meubanco_postgres")
    DB_PORT = get_env("DB_PORT", "5432")
else:
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "https://observatorio.provaconceito.tech",
        "http://observatorio.provaconceito.tech",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]

    # Banco de Dados PostgreSQL Local (Dev)
    DB_NAME = get_env("DEV_DB_NAME", "observatorio_db")
    DB_USER = get_env("DEV_DB_USER", "postgres")
    DB_PASSWORD = get_env("DEV_DB_PASSWORD", "1")
    DB_HOST = get_env("DEV_DB_HOST", "127.0.0.1")
    DB_PORT = get_env("DEV_DB_PORT", "5432")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # para `intcomma`, `naturaltime` nos templates
    "django_user_agents",
    "core",                     # App principal
]

_HAS_WHITENOISE = importlib.util.find_spec("whitenoise") is not None

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    *(["whitenoise.middleware.WhiteNoiseMiddleware"] if _HAS_WHITENOISE else []),
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


# ==============================================================================
# DATABASE
# ==============================================================================
# Permite forçar SQLite via variável de ambiente do sistema (ex: CI do GitHub Actions)
DB_ENGINE = os.environ.get("DB_ENGINE", "postgres").lower()

if DB_ENGINE == "sqlite":
    SQLITE_DIR = BASE_DIR / "sqlite_data"
    SQLITE_DIR.mkdir(parents=True, exist_ok=True)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": SQLITE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if _HAS_WHITENOISE and IS_PROD:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# PROJECT-SPECIFIC CONFIGURATION
# ==============================================================================
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
