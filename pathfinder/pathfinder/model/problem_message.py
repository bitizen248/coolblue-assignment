from pydantic.main import BaseModel


class Point(BaseModel):
    """
    Point in the problem
    """
    name: str
    lat: float
    long: float
    available_from: int | None = None
    available_to: int | None = None


class ProblemMessage(BaseModel):
    """
    Problem message from RabbitMQ
    """
    id: str
    vehicle_count: int = 1
    points: list[Point]
    depot_index: int = 0
