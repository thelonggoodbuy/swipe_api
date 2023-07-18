from pathlib import Path
import environ
import os, sys







BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-nrn6d!_#byk=_e5u8(vwkghwn=#=i-2d1m98+###t!=se3u8y5'

DEBUG = True

ALLOWED_HOSTS = []

# PROJECT_ROOT = os.path.dirname(__file__)
# sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))



INSTALLED_APPS = [
    # Django Framework apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',

    # third part apps
    'rest_framework',
    'rest_framework.authtoken',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'rest_auth',
    # 'rest_auth.registration',
    'drf_spectacular',

    # project apps
    'users.apps.UsersConfig',
    'houses.apps.HousesConfig',
    'ads.apps.AdsConfig',
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env.dev"))



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
 

# ACCOUNT_USERNAME_REQUIRED = False
# AUTHENTICATION_BACKENDS = (
#  "django.contrib.auth.backends.ModelBackend",
#  "allauth.account.auth_backends.AuthenticationBackend",
# )

# SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# from src.houses.views import TokenBearerAuthentication

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSESS': [
        'src.houses.views.TokenBearerAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
                            'rest_framework.permissions.IsAuthenticated',
    ]

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Swipe API',
    'DESCRIPTION': 'Swipe API backend.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'POSTPROCESSING_HOOKS': [],
    'COMPONENT_SPLIT_REQUEST': True,
    # 'SERVE_AUTHENTICATION': ['houses.views.TokenBearerAuthentication',],
    'AUTHENTICATION_WHITELIST': ['houses.views.TokenBearerAuthentication',],
    # "SWAGGER_UI_SETTINGS": {
    #     "deepLinking": True,
    #     "persistAuthorization": True,
    #     "displayOperationId": True,
      
    # },
}