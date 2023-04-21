class Solution:
    """
    A solution to a problem instance.
    Used by the routing algorithm to return a solution
    """

    def __init__(self, id: str, vehicle_solutions: list["VehicleSolution"]):
        self.id = id
        self.vehicle_solutions = vehicle_solutions


class VehicleSolution:
    """
    A solution to a vehicle in a problem instance.
    """

    def __init__(self, distance: float, path: list[dict]):
        self.distance = distance
        self.path = path
