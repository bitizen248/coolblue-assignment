# Mock Delivery 

This is a service for testing `pathfinder` service. 
It's a simple script that generates random points and sends it to the pathfinder service.

## Environment variables
- `MOCKDELIVERY_RABBIT_HOST` - host of RabbitMq 
- `MOCKDELIVERY_RABBIT_PORT` - port of RabbitMq
- `MOCKDELIVERY_RABBIT_USER` - RabbitMq user
- `MOCKDELIVERY_RABBIT_PASSWORD` - RabbitMq password
- `MOCKDELIVERY_RABBIT_VHOST` - RabbitMq vhost
- `MOCKDELIVERY_PROBLEM_QUEUE` - queue for problems


## How to run

```bash
pip3 install poetry
poetry install
poetry run python3 main.py
```
