import json
from json import JSONDecodeError

from pika import BlockingConnection
from pika import BasicProperties
from pydantic.error_wrappers import ValidationError

from pathfinder.model.error import ErrorMessage
from pathfinder.model.problem import Problem
from pathfinder.model.problem_message import ProblemMessage
from pathfinder.model.solution_message import SolutionMessage
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
        self.channel = None

    def _on_new_problem(self, channel, method, properties, body) -> None:
        self.logger.info("Received message")
        problem = body.decode("utf-8")
        try:
            problem = ProblemMessage(**json.loads(problem))
        except JSONDecodeError:
            self.logger.error("Could not decode message")
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                body=ErrorMessage(
                    message="Could not decode message"
                ).json(),
                properties=BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return
        except ValidationError as error:
            self.logger.error("Could not validate message")
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                body=ErrorMessage(
                    message="Could not validate message",
                    additional_info={
                        "errors": error.errors(),
                    }
                ).json(),
                properties=BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return
        problem = Problem(problem)
        solution = self.routing_service.solve_routing_problem(problem)
        self.logger.info("Sending solution")
        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            body=SolutionMessage(solution).json(),
            properties=BasicProperties(
                correlation_id=properties.correlation_id
            )
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_listening(self) -> None:
        self.logger.info("Starting to listen for messages")
        self.channel = self.rabbit_connection.channel()
        self.channel.queue_declare(queue="routing_problem")
        self.channel.basic_consume(
            queue="routing_problem",
            on_message_callback=self._on_new_problem,
            auto_ack=False
        )
        self.channel.start_consuming()

    def stop_listening(self) -> None:
        self.logger.info("Stopping to listen for messages")
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
            self.channel.close()
            self.channel = None
