from typing import Any

from pydantic.main import BaseModel

from pathfinder.model.problem_message import Point
from pathfinder.model.solution import Solution

class VehicleSolutionMessage(BaseModel):
    """
    Vehicle solution
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
                            available_from=point["available_from"],
                            available_to=point["available_to"],
                        )
                        for point in vehicle_solution.path
                    ]
                )
                for vehicle_solution in solution.vehicle_solutions
            ]
        )


