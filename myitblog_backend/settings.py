"""
Django settings for myitblog_backend project.
Modified for Production (Railway + Supabase + Vercel)
"""

from pathlib import Path
import os
import dj_database_url
from urllib.parse import urlparse # Digunakan untuk parsing URL Supabase

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
#  SECURITY CONFIGURATION
# ==============================================================================

# Ambil SECRET_KEY dari Environment Variable Railway.
# Jika tidak ditemukan (di laptop), pakai default key (hanya untuk dev).
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# Otomatis False jika di Railway (Production), True jika di laptop.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Izinkan semua host (Railway menggunakan domain dinamis).
ALLOWED_HOSTS = ['*']


# ==============================================================================
#  APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party libraries
    'rest_framework',
    'django_filters',
    'corsheaders',
    'storages', # [WAJIB] Untuk Supabase Storage (S3)
    
    # Local Apps
    'core',
    'articles',
    'categories',
    'tags',
    'images',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # [WAJIB] Untuk file statis di Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      # [WAJIB] CORS harus paling atas sebelum Common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myitblog_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myitblog_backend.wsgi.application'


# ==============================================================================
#  DATABASE CONFIGURATION (Supabase)
# ==============================================================================

# Otomatis membaca DATABASE_URL dari Railway
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# ==============================================================================
#  VALIDATORS & I18N
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
#  STATIC FILES (CSS, JS) - Whitenoise
# ==============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
#  MEDIA FILES (Supabase Storage / S3)
# ==============================================================================

# Ambil kredensial dari Environment Variables (Railway)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'media' # Pastikan nama bucket di Supabase adalah 'media' (huruf kecil)
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')

# Konfigurasi S3
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False 

# Logika Otomatisasi URL Publik Supabase
if AWS_S3_ENDPOINT_URL:
    try:
        _parsed_url = urlparse(AWS_S3_ENDPOINT_URL)
        _hostname = _parsed_url.netloc
        # Format: https://<domain>/storage/v1/object/public/<bucket>
        AWS_S3_CUSTOM_DOMAIN = f"{_hostname}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
    except Exception:
        AWS_S3_CUSTOM_DOMAIN = None
else:
    AWS_S3_CUSTOM_DOMAIN = None

# Konfigurasi Storage Engine
STORAGES = {
    # Media (Uploads) menggunakan S3/Supabase
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    # Static files tetap menggunakan Whitenoise (Local/Container)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Tentukan URL Media
if AWS_S3_CUSTOM_DOMAIN:
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
else:
    MEDIA_URL = '/media/'
    # Fallback ke sistem file lokal jika S3 tidak dikonfigurasi (misal di laptop tanpa koneksi)
    if not AWS_S3_ENDPOINT_URL:
        STORAGES["default"]["BACKEND"] = "django.core.files.storage.FileSystemStorage"
    
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
#  CORS & SECURITY (Vercel Integration)
# ==============================================================================

# Ganti URL ini dengan domain Vercel Anda yang sebenarnya nanti!
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ravellnetwork.vercel.app",  # Domain Vercel Anda
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://ravellnetwork.vercel.app",             # Domain Frontend
    "https://fandi-beprofile-production.up.railway.app", # Domain Backend (Railway)
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}