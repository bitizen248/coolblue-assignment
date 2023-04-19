class Solution:
    def __init__(
        self, id: str, vehicle_solutions: list["VehicleSolution"]
    ) -> None:
        self.id = id
        self.vehicle_solutions = vehicle_solutions


class VehicleSolution:
    def __init__(self, distance: float, path: list[dict]) -> None:
        self.distance = distance
        self.path = path
