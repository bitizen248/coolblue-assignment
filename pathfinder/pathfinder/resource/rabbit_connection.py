from pika import BlockingConnection
from pika import ConnectionParameters
from pika import PlainCredentials


def rabbit_connection_resource(
    host: str,
    port: int,
    user: str,
    password: str,
    vhost: str = "/",
) -> BlockingConnection:
    connection = BlockingConnection(ConnectionParameters(
        host=host,
        port=port,
        credentials=PlainCredentials(user, password),
        virtual_host=vhost,
    ))
    yield connection
    connection.close()
