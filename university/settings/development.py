from .base import *   # берём всё из base.py

# Переопределяем только то, что отличается в разработке
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# База данных пока оставим SQLite, потом поменяем на PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}