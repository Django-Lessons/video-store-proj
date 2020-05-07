from django.conf import settings


def mode():
    if settings.DEBUG:
        return "sandbox"

    return "live"
