import os
from pathlib import Path
import configparser
from tbgutils import dt as mc_dt


config_file = '/Users/ms/.binocularslive'
if os.path.exists(config_file):
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_file)

    SECRET_KEY = config['DJANGO']['SECRET_KEY']

    POSTGRES_USER = config['POSTGRES']['USER']
    POSTGRES_PASSWORD = config['POSTGRES']['PASS']
    POSTGRES_DB = config['POSTGRES']['DB']

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = config['DJANGO']['DEBUG'].lower() == 'true'
else:
    # This should only be used in github action ci_testing.yml.
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_DB = f"{config['POSTGRES']['DB']}_test"

# Build paths inside the worth like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_VERSIONS = {}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'users',
    'binocularslive.apps.AdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    # 'rest_framework.authtoken',
    'apis',
]

AUTH_USER_MODEL = 'users.Member'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'binocularslive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'binocularslive/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['binocularslive.templatetags.project_tags'],
        },
    },
]

WSGI_APPLICATION = 'binocularslive.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'binocularslive',
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True
mc_dt.time_zone = TIME_ZONE

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'binocularslive/static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
