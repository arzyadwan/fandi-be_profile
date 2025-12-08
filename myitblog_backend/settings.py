"""
Django settings for myitblog_backend project.
Modified for Production (Railway + Supabase + Vercel)
"""

from pathlib import Path
import os
import dj_database_url # [IMPORTANT] Wajib install: pip install dj-database-url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# [MODIFIED] SECURITY WARNING: keep the secret key used in production secret!
# Kita ambil dari Environment Variable Railway. Jika tidak ada (lokal), pakai default tidak aman.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# [MODIFIED] SECURITY WARNING: don't run with debug turned on in production!
# Otomatis False jika di Railway, True jika di laptop Anda (selama tidak set env var DEBUG)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# [MODIFIED] Izinkan host Railway dan Vercel
# '*' mengizinkan semua domain. Aman untuk backend API publik, tapi bisa dipersempit nanti.
ALLOWED_HOSTS = ['*']


# Application definition

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
    
    # Local Apps
    'core',
    'articles',
    'categories',
    'tags',
    'images',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # [IMPORTANT] Wajib untuk serve static files di Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # [IMPORTANT] Pastikan CORS di urutan atas (sebelum CommonMiddleware)
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# [MODIFIED] Database Configuration
# Otomatis membaca DATABASE_URL dari Railway (Supabase)
# Jika di lokal (tidak ada DATABASE_URL), fallback ke db.sqlite3 agar tidak ribet setting postgres lokal
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# [MODIFIED] Konfigurasi Whitenoise untuk Railway

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Tempat kumpul file statis saat collectstatic
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Kompresi file statis

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# [MODIFIED] CORS Configuration (Sangat Penting untuk Vercel)
# Ganti URL di bawah dengan URL Vercel Anda yang sebenarnya nanti!

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",           # Untuk dev lokal
    "http://127.0.0.1:5173",
    "https://ravellnetwork.vercel.app",  
]

# Agar browser mengizinkan cookie/session cross-domain (opsional tapi sering dibutuhkan)
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins (Penting untuk POST request dari Vercel)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://ravellnetwork.vercel.app",
    "https://fandi-beprofile-production.up.railway.app",
]

# Konfigurasi Media Files (Gambar)
# Catatan: Di Railway (file system ephemeral), gambar yang diupload user akan HILANG saat restart/redeploy.
# Untuk solusi permanen, Anda harus pakai Cloudinary atau AWS S3. 
# Untuk sekarang, ini cukup agar tidak error, tapi sadari risikonya.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Konfigurasi Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}