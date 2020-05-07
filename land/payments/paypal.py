from django.conf import settings


def mode():
    if settings.DEBUG:
        return "sandbox"

    return "live"


def get_url_from(iterator, what):
    for link in iterator:
        if link['rel'] == what:
            return link['href']

