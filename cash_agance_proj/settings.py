import os
from pathlib import Path
from dotenv import load_dotenv
import environ
import os

# 1. Bilow nidaamka environ
env = environ.Env()

# 2. HELITAANKA BASE_DIR: Waxaan si toos ah u xaqiijineynaa folder-ka weyn ee mashruuca
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 3. Akhrinta `.env` iyadoo la dammaanad qaadayo meesha uu ku yaalo
# Waxaan u sheegaynaa inuu faylka ku dhex raadiyo folder-ka weyn ee dhabta ah
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)
else:
    # Haddii uu wali ka waayo meeshii saxda ahayd, koodhkan ayaa kuu sheegi doona meesha uu ka rabo
    print(f"⚠️ DIGNIIN: Faylka .env lagama helin meeshan: {env_file}")

# ==============================================================================
# PAYMENT API CONFIGURATION
# ==============================================================================
API_HASH = env('API_HASH', default='fhd.ncbf9hf2ythr') # default ayaa la saaray si uusan u haman
API_CASHIER_PASS = env('API_CASHIER_PASS', default='123123')
API_CASHDESK_ID = env.int('API_CASHDESK_ID', default=77)
API_LOGIN = env('API_LOGIN', default='cashier_login')
API_BASE_URL = env('API_BASE_URL', default='https://partners.servcul.com/CashdeskBotAPI/')
# Soo roridda faylka .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# Maamulka ALLOWED_HOSTS
hosts_input = os.getenv('ALLOWED_HOSTS')
if hosts_input:
    ALLOWED_HOSTS = hosts_input.split(',')
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

LOGIN_URL = 'login'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Tan mar walba ha ka saarin si uusan Render u guban
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cash_agance_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cash_agance_proj.wsgi.application'

# Database - Sida aad u baahneyd ee .env ka aqrinaysa xogta gaarka ah
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization & Waqtiga Soomaaliya
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Mogadishu'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript) ee Live-ka ah
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ammaanka deegaanka rasmiga ah (Production Security)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True