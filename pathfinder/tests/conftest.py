import pytest
from dependency_injector import providers

from pathfinder.container import Container
from tests.mock.rabbit import MockRabbitConnection
from tests.mock.routing_algorithm import MockRoutingAlgorithmService


@pytest.fixture
def container():
    container = Container()
    container.config.from_dict(
        {
            "rabbit_listener": {
                "default_response_queue": "cb.RoutingProblems.Solutions",
                "problems_queue": "cb.RoutingProblems.Problems",
            }
        }
    )
    return container


@pytest.fixture
def mock_rabbit_connection(container):
    with container.rabbit_connection.override(providers.Singleton(
            MockRabbitConnection
    )):
        yield container.rabbit_connection()


@pytest.fixture
def mock_routing_algorithm(container):
    with container.routing_service.override(providers.Singleton(
            MockRoutingAlgorithmService
    )):
        yield container.routing_service()


@pytest.fixture
def test_message():
    with open("tests/data/capitals_problem.json") as f:
        data = f.read()
    return data


@pytest.fixture
def test_message_solution():
    with open("tests/data/capitals_solution.json") as f:
        data = f.read()
    return data
