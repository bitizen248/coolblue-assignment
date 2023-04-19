from dependency_injector.wiring import inject, Provide

from pathfinder.container import Container
from pathfinder.service.rabbit_listener import RabbitListenerService


@inject
def main(
    rabbit_service: RabbitListenerService = Provide[Container.rabbit_service],
):
    """
    Entry point for the application
    Starts the rabbit listener service and finding solution to problem
    """
    try:
        rabbit_service.start_listening()
    except KeyboardInterrupt:
        rabbit_service.stop_listening()

if __name__ == "__main__":
    container = Container()

    container.config.rabbit.host.from_env("PATHFINDER_RABBIT_HOST")
    container.config.rabbit.port.from_env("PATHFINDER_RABBIT_PORT")
    container.config.rabbit.user.from_env("PATHFINDER_RABBIT_USER")
    container.config.rabbit.password.from_env("PATHFINDER_RABBIT_PASSWORD")
    container.config.rabbit.vhost.from_env("PATHFINDER_RABBIT_VHOST")

    container.wire(modules=[__name__])

    main()