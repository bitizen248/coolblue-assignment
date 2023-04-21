# Ivan Dmitriev - assignment for CoolBlue

This is an assignment for the position of Back-end Developer in CoolBlue.
Repository contains:
- `assignment.pdf` - assignment description
- [pathfinder](https://github.com/bitizen248/coolblue-assignment/tree/main/pathfinder) - service for finding the
shortest path between points. Main service for this assignment. To see more details check out README.md in the
service's folder.
- [mockdelivery](https://github.com/bitizen248/coolblue-assignment/tree/main/mockdelivery) - script for generating 
and sending routing problems to pathfinder service. To see more details check out README.md in the service's
folder.
- `docker-compose.yml` - docker-compose file for running pathfinder and mockdelivery services.
- `example.sh` - script for running pathfinder and mockdelivery services. It's setups RabbitMQ and pathfinder service, then
starts mockdelivery script and waits until it's finished. After that, it stops pathfinder service and RabbitMQ.

## ToDo list

### Requirements
- [X] Repository with the project and all infrastructure necessary for running it
- [X] Test of the main service
  - [X] Write mock Rabbit connection
  - [X] Write mock Routing algorithm service
  - [X] RabbitListener unit test
  - [X] Unit test of the algorithm
  - [X] Distances between 2 points unit test
- [X] Docker image for pathfinder service
- [X] example.sh script for running pathfinder and mockdelivery services
- [X] User OR-tools for the routing algorithm
- [X] Documentation

### Bonus
- [ ] RESTful service for sending problems via HTTP
- [X] docker-compose.yml file for running pathfinder and mockdelivery services
- [X] Implement logging
- [X] Support more than 1 vehicle
- [ ] Time constraints for vehicles
