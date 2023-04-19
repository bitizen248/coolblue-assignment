import logging


class BaseService:
    def __init__(self, ):
        self._logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}")
