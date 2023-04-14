from issue_tracker.settings.common import *
import environ

env = environ.Env(  # <-- Updated!
    # set casting, default value
    DEBUG=(bool, False),
)

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Opcions per el deploy
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.fly.dev', '0.0.0.0']  # <-- Updated!

CSRF_TRUSTED_ORIGINS = ['https://*.fly.dev']

DATABASES = {
    'default': env.db()
}