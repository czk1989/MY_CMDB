"""
Django settings for MY_CMDB project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'js194tj3r(9%0^zt54+(k!g6f92gpkzi%hp_lueisx$d1t!lp3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'assets',
    'blog',
    'crm',
    'monitor',
    'news',
    'pic',
    'tasks',
    'web',
    'video',
    'eye',
    'role',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MY_CMDB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'MY_CMDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    "%s/%s" %(BASE_DIR, "static"),
    "%s/%s/%s" %(BASE_DIR, "static",'eye'),

]
ASSET_AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
ASSET_AUTH_HEADER_NAME = 'HTTP_AUTH_KEY'
ASSET_AUTH_TIME = 2

AUTH_USER_MODEL = 'eye.UserProfile'

AUDIT_LOG_DIR = os.path.join(BASE_DIR,'eye/log')
MULTITASK_SCRIPT= os.path.join(BASE_DIR,'tasks/backend/task_runner.py')



DOWNLOAD_DIR = os.path.join(BASE_DIR,'downloads')

REDIS_CONN = {
    'HOST':'192.168.244.128',
    'PORT':6379,
    'DB':0,
    'PASSWORD':'123456',
}

STATUS_DATA_OPTIMIZATION = {
    'latest':[0,20], #0 存储真实数据,600个点
    '10mins':[600,4320], #1m, 每600s进行一次优化，存最大600个点
    '30mins':[1800,4320],#3m
    '60mins':[3600,8760], #365days
}

TRIGGER_CHAN = 'trigger_event_channel'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'czk@126.com'
EMAIL_HOST_PASSWORD = '123456'
DEFAULT_FROM_EMAIL = 'czk<czk@126.com>'

REPORT_LATE_TOLERANCE_TIME = 10 #allow service report late than monitor interval no more than defined seconds.


LOGIN_URL = "/login/"
