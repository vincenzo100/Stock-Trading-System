import os
import dj_database_url
from dotenv import load_dotenv
import pymysql
from pathlib import Path

# Ensure PyMySQL is used instead of MySQLdb
pymysql.install_as_MySQLdb()

# Force load .env file from the correct location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Debugging: Print ENV_PATH to check if Django is looking in the correct location
print(f"Loading .env from: {ENV_PATH}")

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env file not found at {ENV_PATH}. Ensure it's in the correct location.")

load_dotenv(ENV_PATH)  # Ensures Django loads .env

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Debugging: Print SECRET_KEY value (ensure this only runs in local development)
if SECRET_KEY:
    print(f"SECRET_KEY loaded: {SECRET_KEY[:10]}********")  # Only prints part of the key for security

# Ensure SECRET_KEY is set, otherwise raise an error
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY is not set. Please check .env or Railway environment variables.")

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allowed Hosts (Prevents DisallowedHost errors)
ALLOWED_HOSTS = [
    "127.0.0.1",  # Local development
    "localhost",
    "stock-trading-system-production.up.railway.app",  # Railway deployment
]

# CSRF Trusted Origins (For security when sending requests)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",  # Allow local debugging
    "http://localhost",
    "https://stock-trading-system-production.up.railway.app",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # Enables CORS for frontend requests
    'trade_app',  # Your Django application
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Enables CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings (Ensures frontend can make API calls)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local frontend (React, Vue, etc.)
    "http://127.0.0.1:8000",  # Allow local API testing
    "https://stock-trading-system-production.up.railway.app",  # Production backend
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
]

# Database Configuration (MySQL on Railway)
DATABASE_URL = os.getenv('DATABASE_URL')

# Ensure DATABASE_URL is not empty
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check Railway environment variables or .env file.")

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Fix for Django Admin (Ensures it loads properly)
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

# Fix for ROOT_URLCONF
ROOT_URLCONF = "stock_trading.urls"

# WSGI application path
WSGI_APPLICATION = "stock_trading.wsgi.application"
