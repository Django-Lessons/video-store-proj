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

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_PLAN_MONTHLY_ID = os.environ.get('STRIPE_PLAN_MONTHLY_ID')
STRIPE_PLAN_ANNUAL_ID = os.environ.get('STRIPE_PLAN_ANNUAL_ID')
STRIPE_WEBHOOK_SIGNING_KEY = os.environ.get('STRIPE_WEBHOOK_SIGNING_KEY')


PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
PAYPAL_PLAN_MONTHLY_ID = os.environ.get('PAYPAL_PLAN_MONTHLY_ID')
