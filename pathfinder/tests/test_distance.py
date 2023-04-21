from pathfinder.model.problem import Problem


def test_distance_function():
    """
    Test that the distance function works as expected
    """
    assert (
        Problem._calculate_distance(
            {"lat": 0, "long": 0},
            {"lat": 100, "long": 100},
        )
        == 141.4213562373095
    )
