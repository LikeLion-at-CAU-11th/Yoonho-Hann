"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import json
from datetime import timedelta
# from django.core.exceptions import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 소셜로그인 site 설정
    'django.contrib.sites',
]

PROJECT_APPS = [
    'posts',
    'accounts',
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",

    # 소셜로그인 라이브러리
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # allauth.socialaccount.providers.{소셜로그인제공업체}
    # {소셜로그인제공업체} 부분에는 구글 외에도 카카오,네이버 추가 가능
    'allauth.socialaccount.providers.google',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# 사이트는 1개만 사용할 것이라고 명시
SITE_ID = 1

AUTH_USER_MODEL = 'accounts.Member' # AbstractUser 상속 받아서 쓰겠다고 명시

# 나중에 dj_rest_auth.registration.views.SocialLoginView을 쓰기위해 추가
REST_USE_JWT = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username' # username 필드 사용 x
ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False        # username 필드 사용 x
ACCOUNT_AUTHENTICATION_METHOD = 'email'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [ 
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'            # 한국 시간으로 변경

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK ={
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

REST_USE_JWT = True

SIMPLE_JWT  = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),    # 유효 기간 - 3시간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # 유효 기간 - 7일
    'ROTATE_REFRESH_TOKENS': False,         # TokenRefreshView에 Refresh token을 받았을 때 재발급 - 현재는 false
    'BLACKLIST_AFTER_ROTATION': False,      # TokenRefreshView에 Refresh token을 blacklist에 추가 - 현재는 false
    'TOKEN_USER_CLASS': 'accounts.Member',  # 인증할 때 사용할 사용자 class 연결
}