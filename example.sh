docker-compose build
docker-compose up rabbitmq pathfinder -d --wait
docker-compose up mockdelivery
docker-compose down