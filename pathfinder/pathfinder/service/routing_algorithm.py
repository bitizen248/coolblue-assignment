from pathfinder.model.problem import Problem
from pathfinder.model.solution import Solution
from pathfinder.model.solution import VehicleSolution
from pathfinder.service.base import BaseService

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


class RoutingAlgorithmService(BaseService):
    """
    Routing algorithm service
    """

    def solve_routing_problem(self, problem: Problem) -> Solution:
        """
        ✧･ﾟ: *✧･ﾟ:* ･ﾟ✧*:･ﾟ✧
         Magic happens here
        ✧･ﾟ: *✧･ﾟ:* ･ﾟ✧*:･ﾟ✧
        This algorithm is based on the Google OR-Tools library
        """
        # Create routing model
        manager = pywrapcp.RoutingIndexManager(
            problem.get_points_count(),  # Points count
            problem.vehicle_count,  # Vehicles count
            problem.depot_index,  # Depot index
        )
        routing = pywrapcp.RoutingModel(manager)


        # Define weight of each edge
        def distance_callback(from_index, to_index):
            """
            Callback for OR-Tools to measure distance between two points
            """
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return problem.calculate_distance(from_node, to_node)

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback
        )
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        # Setting first solution heuristic (cheapest addition).
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        # Add distance constraint
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Solve the problem and parse the solution.
        solution = routing.SolveWithParameters(search_parameters)
        return self._get_solution(problem, manager, routing, solution)

    @staticmethod
    def _get_solution(
        problem: Problem, manager, routing, solution
    ) -> Solution:
        """
        Get solution from routing model
        """
        vehicle_solutions = []
        for vehicle_id in range(problem.vehicle_count):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            path = []
            while not routing.IsEnd(index):
                path.append(problem.points[manager.IndexToNode(index)])
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)

            path.append(problem.points[manager.IndexToNode(index)])
            plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            vehicle_solutions.append(
                VehicleSolution(distance=route_distance, path=path))
        return Solution(
            id=problem.id,
            vehicle_solutions=vehicle_solutions,
        )
