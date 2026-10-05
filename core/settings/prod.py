from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": int(os.environ["POSTGRES_DB_PORT"]),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}
