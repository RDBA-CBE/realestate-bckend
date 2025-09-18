from .base import *

DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'realestate',
        'USER': 'root',
        'PASSWORD': 'root',  
        'HOST': 'localhost',  
        'PORT': '', 
        'CONN_MAX_AGE': 3600,
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", 
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rdba.testing@gmail.com'
EMAIL_HOST_PASSWORD =  'wddb lkec upei tcbm'
DEFAULT_FROM_EMAIL = 'rdba.testing@gmail.com'

