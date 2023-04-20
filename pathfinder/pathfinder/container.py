from dependency_injector import containers
from dependency_injector import providers

from pathfinder.resource.rabbit_connection import rabbit_connection_resource
from pathfinder.service.rabbit_listener import RabbitListenerService
from pathfinder.service.routing_algorithm import RoutingAlgorithmService


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container.
    Here we define all the resources and services.
    Services can be easily mocked for testing.
    """
    config = providers.Configuration()  # Config object

    # Resources
    rabbit_connection = providers.Resource(
        rabbit_connection_resource,
        host=config.rabbit.host,
        port=config.rabbit.port,
        user=config.rabbit.user,
        password=config.rabbit.password,
        vhost=config.rabbit.vhost,
    )

    # Services
    routing_service = providers.Singleton(RoutingAlgorithmService)
    rabbit_service = providers.Singleton(
        RabbitListenerService,
        rabbit_connection=rabbit_connection,
        routing_service=routing_service,
        default_response_queue=config.rabbit_listener.default_response_queue,
        problems_queue=config.rabbit_listener.problems_queue,
    )
