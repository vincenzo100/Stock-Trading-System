import os
import dj_database_url
from dotenv import load_dotenv
import pymysql
from pathlib import Path

# Ensure PyMySQL is used instead of MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"Loading .env from: {ENV_PATH}")

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)  # Load local .env if available
else:
    print(f"⚠️ WARNING: .env file not found at {ENV_PATH}. Ensure it's in the correct location.")


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if SECRET_KEY:
    print(f"SECRET_KEY loaded: {SECRET_KEY[:10]}********")  #  Only prints part of the key for security

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY is not set. Please check Railway environment variables or .env file.")


DEBUG = os.getenv("DEBUG", "False") == "True"

# Allowed Hosts & CSRF Settings
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "stock-trading-system-production.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "https://stock-trading-system-production.up.railway.app",  # Backend
    "https://stock-trading-system.vercel.app",  # Vercel frontend URL
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",  # Enables CORS for frontend requests
    "trade_app",  # Your Django application
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Enables CORS
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local testing
    "http://127.0.0.1:8000",  # Local testing
    "https://stock-trading-system-production.up.railway.app",  # Backend on Railway
    "https://stock-trading-system.vercel.app",  # Vercel frontend URL
]


CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["content-type", "authorization"]

# Database Configuration (MySQL on Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check Railway environment variables or .env file.")

# Debugging: Print the database URL to verify it's loading correctly
print(f"Using DATABASE_URL: {DATABASE_URL}")

# Parse the database URL correctly for Django
DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Port Configuration for Railway
PORT = os.getenv("PORT", "8000")

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = []

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    STATICFILES_DIRS = [STATIC_DIR]
else:
    STATICFILES_DIRS = []  # Prevents Django from looking for a missing directory

#  Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


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


ROOT_URLCONF = "stock_trading.urls"

#  WSGI application path
WSGI_APPLICATION = "stock_trading.wsgi.application"
