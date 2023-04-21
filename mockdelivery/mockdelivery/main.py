import json
import logging
import os
import random
import sys
import time

from dotenv import load_dotenv
from pika import BasicProperties
from pika import PlainCredentials

from mockdelivery.points import PointsService
from pika import BlockingConnection
from pika import ConnectionParameters


def main():
    """
    Main function
    Sends random points to pathfinder service
    """

    # Load environment variables
    load_dotenv()

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Services declaration
    points_service = PointsService()

    # RabbitMQ connection
    connection = BlockingConnection(
        ConnectionParameters(
            host=os.getenv("MOCKDELIVERY_RABBIT_HOST"),
            port=int(os.getenv("MOCKDELIVERY_RABBIT_PORT")),
            credentials=PlainCredentials(
                os.getenv("MOCKDELIVERY_RABBIT_USER"),
                os.getenv("MOCKDELIVERY_RABBIT_PASSWORD"),
            ),
            virtual_host=os.getenv("MOCKDELIVERY_RABBIT_VHOST"),
        )
    )
    channel = connection.channel()
    queue_name = os.getenv("MOCKDELIVERY_PROBLEM_QUEUE")

    try:
        # Sends 5 different problems to pathfinder
        for _ in range(5):
            # Generate random problem data
            points = points_service.get_random_points()
            vehicle_count = random.randrange(1, 5)
            problem_data = {
                "id": str(random.randrange(1, 100000)),
                "vehicle_count": vehicle_count,
                "depot_index": random.randrange(0, len(points)),
                "points": points,
            }

            # Declaring queue for response
            queue = channel.queue_declare(queue="", auto_delete=True)

            # Send problem data to pathfinder
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(problem_data).encode(),
                properties=BasicProperties(
                    reply_to=queue.method.queue,
                ),
            )

            # Wait for response
            solution_found = False
            for _ in range(10):
                time.sleep(2)
                method_frame, _, body = channel.basic_get(queue=queue.method.queue)
                logger.info(
                    "#" * 60,
                )
                if method_frame:
                    # Solution found!
                    logger.info("Received solution!")
                    response = json.loads(body)

                    # Print solution
                    logger.info("Solution id - %s", response["id"])
                    for i, vehicle in enumerate(response["vehicle_solutions"]):
                        logger.info("Vehicle %s", i)
                        logger.info("Distance - %s", vehicle["distance"])
                        route = " --> ".join(
                            [point["name"] for point in vehicle["path"]]
                        )
                        logger.info("Route:")
                        logger.info(route)
                        logger.info("-" * 60)
                    solution_found = True
                    channel.queue_delete(queue=queue.method.queue)
                    channel.basic_ack(method_frame.delivery_tag)
                    break
            if not solution_found:
                logger.error("Solution not found!")
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Stopping...")

    # Clean up
    channel.close()
    connection.close()


if __name__ == "__main__":
    main()
