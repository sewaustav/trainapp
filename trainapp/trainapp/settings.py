from pathlib import Path
from django.conf.global_settings import LOGIN_REDIRECT_URL
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_TOKEN')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'fitapp.apps.FitappConfig',
    'accounts.apps.AccountsConfig',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#    "http://localhost:8000",         # для Flutter Web в отладке
#    "http://10.0.2.2:8000",          # Android-эмулятор
#    "http://192.168.1.42:3000",      # если Flutter или JS запущен на телефоне
#    "https://your-frontend-app.com", # твой продакшн-домен
# ]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

ROOT_URLCONF = 'trainapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

WSGI_APPLICATION = 'trainapp.wsgi.application'

# потом поменяем на postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=43200),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
}

GOOGLE_IOS_ID = os.getenv('GOOGLE_IOS_ID')
GOOGLE_ANDROID_ID = os.getenv('GOOGLE_ANDROID_ID')
GOOGLE_WEB_ID = os.getenv('GOOGLE_WEB_ID')

GOOGLE_CLIENT_ID = GOOGLE_WEB_ID
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
FLUTTER_WEB_REDIRECT_URL='http://127.0.0.1:8888'

# GOOGLE_CLIENT_IDS = [
#     GOOGLE_ANDROID_ID,
#     GOOGLE_IOS_ID,
#     GOOGLE_WEB_ID,
# ]


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '272622672076-6bbi7ekh8q25a5ng0ucolovouhbf2n91.apps.googleusercontent.com',
            'secret': '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',
        },
        # 'SCOPE': ['profile', 'email', ],
        # 'AUTH_PARAMS': {'access_type': 'online'},
        # 'METHOD': 'oauth2',
        # 'VERIFIED_EMAIL': True,
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True

# LOGIN_REDIRECT_URL='login'
