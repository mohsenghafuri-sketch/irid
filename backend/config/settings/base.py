from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY", default="change-me")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

#ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])
ALLOWED_HOSTS = [
    "localhost",
    ".localhost",       # این تمام زیردامنه‌ها مثل irid.localhost را پوشش می‌دهد
    "127.0.0.1",
    "192.168.10.85",    # آی‌پی سرور تو
]

SHARED_APPS = [
    "django_tenants",

    # Project shared apps
    "apps.tenants",
    "apps.accounts",

    # Django shared apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party shared apps
    "rest_framework",
]

TENANT_APPS = [
    # Django apps needed in tenant schemas
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tenant business apps
    "apps.accounts",
    "apps.correspondence",
    "apps.forms",
    "apps.workflow",
    "apps.requests",
]

INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]


# در فایل backend/config/settings/base.
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": env("POSTGRES_DB", default="automation"),
        "USER": env("POSTGRES_USER", default="automation"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="change-me-db-password"),
        "HOST": env("POSTGRES_HOST", default="postgres"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

DATABASE_ROUTERS = (
    "django_tenants.routers.TenantSyncRouter",
)

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = "tenants.Domain"

# Force tenants to use the same URLConf as public for now
PUBLIC_SCHEMA_URLCONF = 'config.urls'

PUBLIC_SCHEMA_NAME = "public"
AUTH_USER_MODEL = "accounts.User"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://irid.localhost:8000",
    "http://192.168.10.85:8000",
    "http://192.168.10.85:5173",  # اضافه کردن آدرس فرانت‌اند
]

# همچنین مطمئن شو CORS هم این مورد را پوشش می‌دهد
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://192.168.10.85:8000",
    "http://192.168.10.85:5173",  # اضافه کردن آدرس فرانت‌اند
]
