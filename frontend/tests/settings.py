"""Isolated UI verification only. Never imports .env or connects to the live DB."""
from pathlib import Path
from tempfile import gettempdir

BASE_DIR = Path(__file__).resolve().parents[2]
SECRET_KEY = "isolated-ui-test-key-not-for-deployment"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
                 "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
                 "accounts.apps.AccountsConfig", "dictionary.apps.DictionaryConfig",
                 "quiz.apps.QuizConfig", "core.apps.CoreConfig", "errorHandler.apps.ErrorhandlerConfig"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
              "core.middleware.InterfaceLanguageMiddleware", "django.middleware.common.CommonMiddleware",
              "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
              "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True, "DIRS": [],
              "OPTIONS": {"context_processors": ["django.template.context_processors.request",
                  "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages",
                  "core.context_processors.unread_event_count", "core.context_processors.unreply_feedback_count"]}}]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": Path(gettempdir()) / "kotoba-ui-validation.sqlite3"}}
AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(gettempdir()) / "kotoba-ui-media"
LOGIN_URL = "/accounts/user_login/"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
DEFAULT_FROM_EMAIL = "ui-test@example.test"
ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS = 60
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
AUTH_PASSWORD_VALIDATORS = []
