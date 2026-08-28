import os

os.environ.setdefault("SECRET_KEY", "test-only-secret-key")

from .settings import *  # noqa: E402,F403

# Use SQLite in-memory database for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Speed up password hashing
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
