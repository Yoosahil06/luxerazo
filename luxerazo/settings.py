import os
from pathlib import Path

# --------------------------------------------
# BASE DIR
# --------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------
# SECURITY
# --------------------------------------------
SECRET_KEY = 'django-insecure-bll9(2xl5-+nrk()f$_c!z+fqy2sk(503k4^yt0pj^&&*6_*e6'
DEBUG = True
ALLOWED_HOSTS = [ '13.220.153.37', 'luxerazo.com', 'www.luxerazo.com', '127.0.0.1']

# --------------------------------------------
# INSTALLED APPS
# --------------------------------------------
INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'products',
    'orders',
    'users',
    'brands',
    'concierge',
    'catalog',
    'cms',
    'analytics',
    # 'accounts',
    # 'dashboard',
    # 'content',
    # 'utils',

    'djmoney',
    'django_countries',
]

# --------------------------------------------
# MIDDLEWARE
# --------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------
# ROOT URL CONFIG
# --------------------------------------------
ROOT_URLCONF = 'luxerazo.urls'

# --------------------------------------------
# TEMPLATES
# --------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates
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

# --------------------------------------------
# WSGI
# --------------------------------------------
WSGI_APPLICATION = 'luxerazo.wsgi.application'

# --------------------------------------------
# DATABASE (PostgreSQL)
# --------------------------------------------
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Luxerazo',
        'USER': 'postgres',
        'PASSWORD': 'Sahil096114',  
        'HOST': 'localhost',     
        'PORT': '5432',
    }
}


# --------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------
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

# --------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --------------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = '/home/ubuntu/luxerazo/staticfiles'
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# --------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------
# AUTHENTICATION SETTINGS
# --------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'
