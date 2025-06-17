# settings.py — completo para dev (SQLite)
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ──────────────────────────────────────────────────────────────
#  Apps
# ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Core Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Terceiros
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_tailwind",
    "tailwind",  # Added tailwind
    "rolepermissions",
    "admin_interface",
    "colorfield",

    # Apps locais
    "core.apps.CoreConfig",  # onde estão os modelos (Mandato, etc.)
    "theme",  # onde estão os temas (cores, fontes, etc.)
]

SITE_ID = 1

# Tailwind CSS
TAILWIND_APP_NAME = 'theme' # Added TAILWIND_APP_NAME

# ──────────────────────────────────────────────────────────────
#  Backends & Auth
# ──────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "core.User"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
LOGIN_REDIRECT_URL = "/inicio/" # Ensure this points to the welcome page after login
LOGIN_URL = "/contas/login/"    # Allauth's default login URL

# RolePermissions
ROLEPERMISSIONS_MODULE = "config.roles"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ["tailwind"]
CRISPY_TEMPLATE_PACK = "tailwind"

# ──────────────────────────────────────────────────────────────
#  URLs
# ──────────────────────────────────────────────────────────────
ROOT_URLCONF = "urls"

# ──────────────────────────────────────────────────────────────
#  Middleware
# ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware"
]

# ──────────────────────────────────────────────────────────────
#  Templates
# ──────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # necessário p/ allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ──────────────────────────────────────────────────────────────
#  Database (SQLite dev)
# ──────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ──────────────────────────────────────────────────────────────
#  Internationalization
# ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────
#  Static / Media
# ──────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "theme/static", # Add this line
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────────────────────────────
#  Default primary key field type
# ──────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AssessorAI API
AI_API_BASE_URL = "https://assessorai.fly.dev"
AI_API_KEY = os.getenv("AI_API_KEY", "12345")
