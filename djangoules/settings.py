
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'f9!fdoms=&$h%9yy-i6_b8pla-y4zo^^2@8c(it8^kmbnk8pqa'

DEBUG = False

LOGIN_REDIRECT_URL = '/login/'




INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'corsheaders',
    'motorapp',
    'frontapp',
    'webapp',
    'mobapp',
    'dinamicasapp',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
    
)

ROOT_URLCONF = 'djangoules.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoules.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'telcel.sqlite3'),
    }
}



LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


LOGIN_URL = "/login/"
LOGIN_REDIRECT_VIEW = "/"
LOGOUT_URL = "/logout/"


CORS_ORIGIN_ALLOW_ALL = True


CORS_ORIGIN_WHITELIST = (
    'experienciastelcel.com',
    '45.33.11.198',
    'admin.experienciastelcel.com',
)


ALLOWED_HOSTS = ['45.33.11.198','experienciastelcel.com','admin.experienciastelcel.com']
#ALLOWED_HOSTS = ['localhost', '127.0.0.1','experienciastelcel.com']

#CORS_ALLOW_CREDENTIALS = True

try:
    from local_settings import *
except ImportError:
    pass

