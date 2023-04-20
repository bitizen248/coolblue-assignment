import logging
import sys


class BaseService:
    """
    Base class for all services
    Have logging and possibly to add other common functionality
    """
    def __init__(self, ):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)