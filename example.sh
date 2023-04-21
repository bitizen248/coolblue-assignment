# Script to run services for the example.
# Its starts the rabbitmq, pathfinder and launches mockdelivery script
docker-compose build
docker-compose up rabbitmq pathfinder -d --wait
docker-compose up mockdelivery
docker-compose down