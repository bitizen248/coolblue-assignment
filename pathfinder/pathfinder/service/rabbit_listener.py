import json

from pika import BlockingConnection
from pika import BasicProperties
from pydantic.error_wrappers import ValidationError

from pathfinder.model.error import ErrorMessage
from pathfinder.model.problem import Problem
from pathfinder.model.problem_message import ProblemMessage
from pathfinder.model.solution_message import SolutionMessage
from pathfinder.service.base import BaseService
from pathfinder.service.routing_algorithm import RoutingAlgorithmService
from pathfinder.utils import rabbit_callback


class RabbitListenerService(BaseService):
    """
    RabbitMQ listener service
    Listens for new problems and sends solutions back
    """

    def __init__(
        self,
        rabbit_connection: BlockingConnection,
        routing_service: RoutingAlgorithmService,
        default_response_queue: str,
        problems_queue: str,
    ) -> None:
        super().__init__()
        self.problems_queue = problems_queue
        self.default_response_queue = default_response_queue
        self.routing_service = routing_service
        self.rabbit_connection = rabbit_connection
        self.channel = None

    @rabbit_callback
    def _on_new_problem(
        self, channel, method, properties, body
    ) -> ErrorMessage | None:
        """
        Callback for new problem messages
        If callback returns an error message, it will be sent back to the client
        """
        self.logger.info("Received message")
        problem = body.decode("utf-8")
        try:
            problem = ProblemMessage(**json.loads(problem))
        except json.JSONDecodeError:
            self.logger.error("Could not decode message")
            return ErrorMessage(
                message="Could not decode message"
            )
        except ValidationError as error:
            self.logger.error("Failed to parse message")
            return ErrorMessage(
                message="Failed to parse message",
                details={
                    "errors": error.errors(),
                }
            )
        self.logger.info("Solving problem")
        problem = Problem(problem)
        solution = self.routing_service.solve_routing_problem(problem)
        self.logger.info("Sending solution")
        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to or self.default_response_queue,
            body=SolutionMessage(solution).json(),
            properties=BasicProperties(
                correlation_id=properties.correlation_id
            )
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _nack_message_with_error(
        channel, properties, method, error: ErrorMessage
    ) -> None:
        """
        NACK a message with an error message
        """
        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            body=error.json(),
            properties=BasicProperties(
                correlation_id=properties.correlation_id
            )
        )
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_listening(self) -> None:
        """
        Start listening for messages
        """
        self.logger.info("Starting to listen for messages")
        self.channel = self.rabbit_connection.channel()

        # Here we can declare DLX for problematic messages

        self.channel.queue_declare(queue=self.problems_queue, durable=True)
        self.channel.basic_consume(
            queue=self.problems_queue,
            on_message_callback=self._on_new_problem,
            auto_ack=False
        )
        self.channel.start_consuming()

    def stop_listening(self) -> None:
        """
        Stop listening for messages
        """
        self.logger.info("Stopping to listen for messages")
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
            self.channel.close()
            self.channel = None
