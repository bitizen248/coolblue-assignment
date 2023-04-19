from pika import BlockingConnection

from pathfinder.service.base import BaseService
from pathfinder.service.routing_algorithm import RoutingAlgorithmService


class RabbitListenerService(BaseService):
    def __init__(
        self,
        rabbit_connection: BlockingConnection,
        routing_service: RoutingAlgorithmService,
    ) -> None:
        super().__init__()
        self.routing_service = routing_service
        self.rabbit_connection = rabbit_connection
