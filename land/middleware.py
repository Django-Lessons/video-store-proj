import logging


logger = logging.getLogger(__name__)


class RequestLogger:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        logger.info(
            f"{request.method} path={request.path}"
        )

        return response
