from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.local.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rdba.testing@gmail.com'
EMAIL_HOST_PASSWORD =  'wddb lkec upei tcbm'
DEFAULT_FROM_EMAIL = 'rdba.testing@gmail.com'