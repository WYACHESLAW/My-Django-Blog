import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vj%ntqsa8wvhpteplow+s#%s)#=gazbw-%0#ye76#0hr@=^7pi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com', '198.162.104.4', 'tut.by']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'blog',
    'taggit',
    'django_cleanup',
    'easy_thumbnails',
    'captcha',
    'main'
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

ROOT_URLCONF = 'mysite.urls'

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
                'blog.middlewares.post_context_processor',
                'main.middlewares.st_context_processor',
                'main.middlewares.std_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

#DATABASES = {
#'default': {
#    'ENGINE': 'django.db.backends.postgresql_psycopg2',
#    'NAME': 'dbblog',
#    'USER': 'postgres',
#    'PASSWORD': '14111951',
#    'HOST': '',
#    'PORT':'5432',
#    }
#}
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'blog.AdvUser'
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
THUMBNALL_ALIASES = {
    '': {
        'default': {
            'size': (96, 96),
            'crop': 'scale',
        },
    },
}
Login_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
THUМВNAIL_BASEDIR = 'thumbnails'
МEDIA_ROOT = os.path.join(BASE_DIR, 'media')
МEDIA_URL = '/media/'
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')