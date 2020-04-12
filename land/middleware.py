import logging


logger = logging.getLogger(__name__)


class RequestLogger1:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        logger.info("BEFORE RL1")

        response = self.get_response(request)

        logger.info("AFTER RL1")

        return response


class RequestLogger2:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        logger.info("BEFORE RL2")

        response = self.get_response(request)

        logger.info("AFTER RL2")
        logger.info(f"method={request.method} path={request.path}")

        return response
