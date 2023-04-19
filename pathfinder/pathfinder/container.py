from dependency_injector import containers, providers

from pathfinder.resource.rabbit_connection import rabbit_connection_resource
from pathfinder.service.rabbit_listener import RabbitListenerService
from pathfinder.service.routing_algorithm import RoutingAlgorithmService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    rabbit_connection = providers.Resource(
        rabbit_connection_resource,
        host=config.rabbit.host,
        port=config.rabbit.port,
        user=config.rabbit.user,
        password=config.rabbit.password,
    )

    routing_service = providers.Singleton(RoutingAlgorithmService)
    rabbit_service = providers.Singleton(
        RabbitListenerService,
        rabbit_connection=rabbit_connection,
        routing_service=routing_service
    )
