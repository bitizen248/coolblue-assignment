class MockRabbitConnection:
    def __init__(self) -> None:
        self.declared_queues = list()
        self.consumers = dict()
        self.is_listening = False
        self.messages = list()

    def channel(self):
        return self

    def queue_declare(self, **kwargs):
        self.declared_queues.append(kwargs)

    def basic_consume(self, queue, on_message_callback, **_):
        self.consumers[queue] = on_message_callback

    def start_consuming(self):
        self.is_listening = True

    def stop_consuming(self):
        self.is_listening = False

    def close(self):
        pass

    def is_open(self):
        return self.is_listening

    def basic_publish(self, **kwargs):
        self.messages.append(kwargs)

    def basic_ack(self, **kwargs):
        pass

    def basic_nack(self, **kwargs):
        pass

    def call_callback(self, queue, body, relpy_to=None):
        self.consumers[queue](self, MockRabbitMethod(), MockProperties(relpy_to), body)


class MockRabbitMethod:
    @property
    def delivery_tag(self):
        return 1


class MockProperties:
    def __init__(self, reply_to=None):
        self.reply_to = reply_to

    @property
    def correlation_id(self):
        return 1
