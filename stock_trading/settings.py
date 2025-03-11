from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Change to False in production

# Allowed Hosts (Fixes DisallowedHost error)
ALLOWED_HOSTS = [
    "127.0.0.1",  # Local development
    "stock-trading-system-production.up.railway.app",  # Railway domain
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
    'trade_app',
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
    "http://localhost:3000",  # Local frontend
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

# Database configuration (Modify if using PostgreSQL on Railway)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
