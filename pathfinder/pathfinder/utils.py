from pika import BasicProperties

from pathfinder.model.error import ErrorMessage


def rabbit_callback(func):
    """
    Decorator for rabbitmq callbacks
    Catches exceptions and sends error message back to the client
    """

    def wrapper(self, channel, method, properties, body):
        try:
            error = func(self, channel, method, properties, body)
        except Exception as e:
            self.logger.error("Error processing message", exc_info=e)
            error = ErrorMessage(
                message="Error processing message. Check logs for details",
            )

        if error:
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to or self.default_response_queue,
                body=error.json(),
                properties=BasicProperties(correlation_id=properties.correlation_id),
            )
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    return wrapper
