from pathfinder.model.solution import Solution
from pathfinder.model.solution import VehicleSolution


class MockRoutingAlgorithmService:
    def solve_routing_problem(self, *_, **__):
        return Solution(
            id="mock",
            vehicle_solutions=[
                VehicleSolution(
                    distance=123,
                    path=[
                        {"name": "1", "lat": 1, "long": 1, "available_from": 1, "available_to": 1},
                    ],
                ),
            ],
        )
