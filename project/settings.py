import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!t)t=4ea$=1^057du@1qnjww_kuj$qe(!9$@r7)7(8buz3hodd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    'api_user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # corsheaders
    'django.middleware.csrf.CsrfViewMiddleware',  # クロスサイトリクエストフォージェリ（CSRF）対策を有効にする
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
    # パスワードの複雑さを強化
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            # パスワードの長さを設定
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        # 匿名ユーザーは1時間に100リクエストまで、認証済みユーザーは1時間に1000リクエストまで制限
        'anon': '100/hour',
        'user': '1000/hour'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # アクセストークンの有効期限
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # リフレッシュトークンの有効期限
    'ROTATE_REFRESH_TOKENS': True,                   # リフレッシュトークンを更新するかどうか
    'BLACKLIST_AFTER_ROTATION': True,                # 更新後に古いトークンをブラックリストに追加するかどうか
}

# クリックジャッキング対策を有効にする
X_CONTENT_TYPE_OPTIONS = 'nosniff'
X_FRAME_OPTIONS = 'DENY'
X_XSS_PROTECTION = '1; mode=block'

# セッションクッキーのセキュリティ設定を強化する
# SESSION_COOKIE_SECURE = True  # セッションクッキーをHTTPS経由でのみ送信する
# CSRF_COOKIE_SECURE = True     # CSRFクッキーをHTTPS経由でのみ送信する


# セキュリティヘッダーの設定
SECURE_CONTENT_TYPE_NOSNIFF = True      # MIMEタイプのスニッフィングを防止する
SECURE_BROWSER_XSS_FILTER = True        # XSSフィルタを有効にする
SECURE_REFERRER_POLICY = 'same-origin'  # 同一オリジンポリシーを適用する

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:9000"
]

# Logging
# ログの保存場所を指定
LOG_DIRECTORY = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',  # ログレベルを本番環境用に調整
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'production.log'),
            'when': 'midnight',  # ログローテーションのタイミングを指定
            'interval': 7,  # 7日ごとにログローテーションを実行
            'backupCount': 1000,  # 保存するログファイルの数
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',  # ログレベルを本番環境用に調整
            'propagate': True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# use customUser
AUTH_USER_MODEL = "api_user.User"

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'your_email_host'  # SMTPサーバーのホスト名
# EMAIL_PORT = 587                # SMTPサーバーのポート番号
# EMAIL_USE_TLS = True            # TLS接続を使用する
# EMAIL_HOST_USER = 'your_email_address'    # 送信元メールアドレス
# EMAIL_HOST_PASSWORD = 'your_email_password'  # 送信元メールアドレスのパスワード
# DEFAULT_FROM_EMAIL = 'your_email_address'   # 送信元のデフォルトメールアドレス
