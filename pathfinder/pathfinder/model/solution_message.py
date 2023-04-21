from typing import Any

from pydantic.main import BaseModel

from pathfinder.model.problem_message import Point
from pathfinder.model.solution import Solution


class VehicleSolutionMessage(BaseModel):
    """
    Vehicle solution message to RabbitMQ
    """
    distance: float
    path: list[Point]


class SolutionMessage(BaseModel):
    """
    Solution message to RabbitMQ
    """
    id: str
    vehicle_solutions: list[VehicleSolutionMessage]

    def __init__(__pydantic_self__, solution: Solution) -> None:
        """
        Constructor from solution object of the algorithm
        """
        super().__init__(
            id=solution.id,
            vehicle_solutions=[
                VehicleSolutionMessage(
                    distance=vehicle_solution.distance,
                    path=[
                        Point(
                            name=point["name"],
                            lat=point["lat"],
                            long=point["long"],
                        )
                        for point in vehicle_solution.path
                    ]
                )
                for vehicle_solution in solution.vehicle_solutions
            ]
        )
