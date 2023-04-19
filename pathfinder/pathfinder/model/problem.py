import math

from pathfinder.model.problem_message import ProblemMessage


class Problem:

    def __init__(self, problem_message: ProblemMessage):
        self.id = problem_message.id
        self.vehicle_count = problem_message.vehicle_count
        self.points = dict()
        for i, point in enumerate(problem_message.points):
            self.points[i] = {
                "name": point.name,
                "lat": point.lat,
                "long": point.long,
                "available_from": point.available_from,
                "available_to": point.available_to,
            }
        self.depot_index = problem_message.depot_index

    def calculate_distance(self, a_index: int, b_index: int) -> int:
        a = self.points[a_index]
        b = self.points[b_index]
        return int(self._calculate_distance(a, b))

    def _calculate_distance(self, a: dict, b: dict) -> float:
        return math.sqrt(
            (a["lat"] - b["lat"]) ** 2 + (a["long"] - b["long"]) ** 2
        )

    def get_points_count(self) -> int:
        return len(self.points)