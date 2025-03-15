from pathlib import Path
import os
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')  # Use environment variable for security

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Set DEBUG via env variables for flexibility

# Allowed Hosts (Fixes DisallowedHost error)
ALLOWED_HOSTS = [
    "127.0.0.1",  # Local development
    "stock-trading-system-production.up.railway.app",  # Railway deployment
]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
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
    'corsheaders',  # Enables CORS
    'trade_app',  # Your Django app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Ensures CORS is enabled
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
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'mysql://your_db_user:your_db_password@your-db-host:3306/stock_trading_system'),
        conn_max_age=600,  # Helps with persistent connections
    )
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
        "DIRS": [],  # Can add custom template directories here if needed
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
