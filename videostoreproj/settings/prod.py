from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# In production you need to run
# ./manage collectstatic to gather all static files
# in STATIC_ROOT
STATIC_ROOT = '/demo/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'xyz_console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'land.middleware': {
            'handlers': ['xyz_console'],
            'level': 'INFO'
        }
    }
}
