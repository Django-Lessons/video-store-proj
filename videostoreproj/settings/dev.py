from .base import *

DEBUG = True

MEDIA_ROOT = '/demo/media'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'xyz_console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'land': {
            'handlers': ['xyz_console'],
            'level': 'DEBUG'
        }
    }
}
