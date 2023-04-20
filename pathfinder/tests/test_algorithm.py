import json

from pathfinder.model.problem import Problem
from pathfinder.model.problem_message import ProblemMessage
from pathfinder.model.solution_message import SolutionMessage


def test_routing_algorithm(container, test_message, test_message_solution):
    """
    Test that the routing algorithm service works as expected
    """
    problem = ProblemMessage(**json.loads(test_message))
    problem = Problem(problem)
    solution = container.routing_service().solve_routing_problem(problem)
    solution = SolutionMessage(solution)
    expected_solution = json.loads(test_message_solution)
    assert solution.dict() == expected_solution
