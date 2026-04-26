import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-**4w^b+fuxj5lk^lrk57jp&-ehz_(t3g+i#at-646l^efun-%x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://test.armariotec.com.br',]
ALLOWED_HOSTS = ['*']


LOGOUT_REDIRECT_URL = '/login/'
SITE_ID             = 1                         # alguns plugins precisam dessa informação
SYSTEM_NAME         = 'ArmárioTec'              # incluido para facilitar o nome nas views
#AUTH_USER_MODEL     = "accounts.CustomUser"     # ALTERAR O MODELO PADRAO DE USUARIO DO DJANGO!
LOGIN_URL           = 'accounts:login'          # nao logados serao direcionados para esse endereço
LOGIN_REDIRECT_URL  = '/'                       # endreço apos o login
LOGOUT_REDIRECT_URL = 'accounts:login'          # endereço apos logout
MAX_DEPENDENT_HU    = 15                        # maximo possivel de dependentes em um apto
TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", default='change-me')                   # lembrar de carregar no environment
TELEGRAM_BOT_URL    = os.environ.get("TELEGRAM_BOT_URL", default='724cadb4-d8b1-48e8-8f08-9d06092f9763/')  # UUID4. gerar um para usar como url do bot.
URL_CLOUD_SYSTEM    = os.environ.get("URL_CLOUD_SYSTEM", default='test.armariotec.com.br')  # url base do sistema de clientes
# webauthn
WEBAUTH_RP_ID = os.environ.get("WEBAUTH_RP_ID", default='test.armariotec.com.br')  # the hostname (minus scheme and port) of the server running your Django app
WEBAUTH_RP_NAME = os.environ.get("WEBAUTH_RP_NAME", default='ArmarioTec')  # human readable name of your server intended only for display
WEBAUTH_ORIGIN = os.environ.get("WEBAUTH_ORIGIN", default='https://test.armariotec.com.br')  # origin do webauthn

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #3rd party apps
    'pwa',
    #Local apps
    'accounts',

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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['app/templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images, ...)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (Images, Files)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DJANGO PWA CONFIGURATION ==========================================
PWA_APP_DEBUG_MODE = False # Set to False if you want the service worker to work when DEBUG = False
PWA_APP_NAME = 'My App'
PWA_APP_DESCRIPTION = "My app description"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'Shortcut',
        'url': '/target',
        'description': 'Shortcut to a page in my application'
    }
]
PWA_APP_SCREENSHOTS = [
    {
      'src': '/static/images/icons/splash-750x1334.png',
      'sizes': '750x1334',
      "type": "image/png"
    }
]