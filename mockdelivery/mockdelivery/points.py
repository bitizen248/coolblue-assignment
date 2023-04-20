import json
import random


class PointsService:
    """
    Service for getting random points
    """
    def __init__(self):
        with open("points.json", "r") as file:
            points_data = json.load(file)
        self.points = points_data["points"]

    def get_random_points(self):
        """
        Get random points
        """
        points_count = random.randrange(4, len(self.points))
        random.shuffle(self.points)
        return self.points[:points_count]
