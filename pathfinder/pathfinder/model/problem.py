import math

from pathfinder.model.problem_message import ProblemMessage


class Problem:
    """
    Problem model for algorithm to solve
    """

    def __init__(self, problem_message: ProblemMessage):
        """
        Constructor form problem message
        """
        self.id = problem_message.id
        self.vehicle_count = problem_message.vehicle_count
        self.points = list()
        for point in problem_message.points:
            self.points.append({
                "name": point.name,
                "lat": point.lat,
                "long": point.long,
                "available_from": point.available_from,
                "available_to": point.available_to,
            })
        self.depot_index = problem_message.depot_index

    def calculate_distance(self, a_index, b_index) -> int:
        """
        Callback for OR-Tools
        Calculate distance between two points
        """
        a = self.points[a_index]
        b = self.points[b_index]
        # float doesn't work with OR-Tools, so we need to cast to int
        return int(self._calculate_distance(a, b))

    @staticmethod
    def _calculate_distance(a: dict, b: dict) -> float:
        """
        Calculate distance between two points
        """
        return math.sqrt(
            (a["lat"] - b["lat"]) ** 2 + (a["long"] - b["long"]) ** 2
        )

    def get_points_count(self) -> int:
        """
        Get points count
        """
        return len(self.points)