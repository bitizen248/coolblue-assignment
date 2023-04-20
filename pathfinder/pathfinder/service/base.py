import logging


class BaseService:
    """
    Base class for all services
    Have logging and possibly to add other common functionality
    """
    def __init__(self, ):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}")