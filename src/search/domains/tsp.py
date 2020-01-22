"""TSP domain.

Typical use:

    state_1 = tsp.State( . . . )
    state_2 = tsp.State( . . . )
    h = tsp.cost(state_1, state_2, *problem variable*)
"""

from collections import namedtuple
from itertools import product
import math
import random

from src.search.utils.datastructures import Problem

Point = namedtuple('Point', 'x y')
City = namedtuple('City', 'point visited')


class State:
    """State class specific to TSP domain.

    A TSP state is a list of cities accompanied by labels describing
    whether or not a city has been visited, and whether a city is the
    'current' city. A 1 or -1 (depending on direction in which state
    is expanded) indicates that a city has been visited, and a label
    of 0 shows a city as the current city.

    The initial city is shown twice in a state, as a TSP solution
    sees this city twice.

    Includes successor function, as well as hash and equality
    __ methods.

    Attributes:
        state: Immutable variable containing the state description.
        n_successors: Number of successors of the state.
        successors_list: Lazily-calculated list of (state, cost)
            tuples, as the successors of self.
    """

    def __init__(self, state, direction, n_successors):
        """Initializes State object."""
        self.state = state
        self.direction = direction
        self.n_successors = len([i for i in state if i.visited == -1*direction])
        self.successors_list = None

    def successors(self, problem):
        """Get successors of self, sorted by cost.

        Lazily calculates the successors. If function hasn't been
        called before, successors are calculated and stored.
        If stored list exists, it is simply retrieved.

        Successors of a given state are the configurations of cities
        which directly follow from the current state. The current city,
        initially labelled 0, is relabelled to show that it has been
        visited. The new current city is relabelled 0.

        Args:
            problem: namedtuple object as created in parse_problem().

        Returns:
            A sorted list of the successors of self.
        """
        if self.successors_list is None:
            self.successors_list = []
            for idx, city in enumerate(self.state):
                if city.visited == 0:
                    current_city = city
                    current_city_idx = idx
                    break
            else:
                raise IndexError('No city found with visited == 0')

            """ Get successor states, costs and append as (state, cost) to self.successors_list """
            for idx, city in enumerate(self.state):
                if city.visited == -1*self.direction:
                    new_current_city_idx = idx
                    new_state = list(self.state)
                    new_state[current_city_idx] = new_state[current_city_idx]._replace(visited=self.direction)
                    new_state[new_current_city_idx] = new_state[new_current_city_idx]._replace(visited=0)
                    new_state = State(tuple(new_state), self.direction, n_successors=self.n_successors-1)
                    c = _dist(current_city.point, city.point)
                    self.successors_list.append((new_state, c))

            self.successors_list = sorted(self.successors_list, key=lambda x: x[1])
        return self.successors_list

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f'State({self.state})'

    def __eq__(self, other):
        return self.state == other.state


def parse_problem(problem_str):
    """Create namedtuple instance of specified problem.

    Creates a namedtuple instance containing various information about
    the problem, including initial state, goal state, and epsilon
    (minimum operator cost).

    Args:
        problem_str: A string representation of the problem, { . . . }

    Returns:
        A namedtuple containing problem information.
    """
    cities = [Point(*map(float, coords.split(' '))) for coords in problem_str.split(',')]
    # initial_city = Point(*map(float, cities[0].split(' ')))

    initial_tuple = (City(cities[0], 0),) \
                    + tuple(City(cities[i], -1) for i in range(1, len(cities))) \
                    + (City(cities[0], -1),)

    goal_tuple = (City(cities[0], 1),) \
                 + tuple(City(cities[i], 1) for i in range(1, len(cities))) \
                 + (City(cities[0], 0),)

    epsilon = _get_epsilon(cities)
    problem = Problem(initial=State(initial_tuple, direction=1, n_successors=len(cities)-1),
                      goal=State(goal_tuple, direction=-1, n_successors=len(cities)-1),
                      epsilon=epsilon,
                      statics=(cities,))
    return problem


def generate_problems(config):
    """Generates a set of arbitrary-pancake problems.

    Generates a set of arbitrary-pancake problems as per the problem
    generation information specified in the config file.

    Either generates the problems from a string given in a file (with
    filepath specified in config file), or randomly generates a set
    number of problems.

    Args:
        config: A parsed config file.

    Returns:
        A list of namedtuple instances representing {domain name}
            problems.
    """
    problems = []
    if config.settings['precompiled']:
        for file_name in config.settings['precompiled']:
            with open(file_name, 'r') as f:
                problem_str = ','.join(line.strip('\n') for line in f.readlines())
                problems.append(parse_problem(problem_str))
    else:
        try:
            n_problems = config.settings['n_problems']
            param = config.settings['param']
        except KeyError:
            raise Exception("For config file specifying no precompiled problem, ensure parameters 'params', "
                            "'n_problems' are set'")
        for p in range(n_problems):
            """Generate problem and append to problems"""
            problem_str = ','.join([f'{round(random.uniform(0, 1000), ndigits=3)} '
                                    f'{round(random.uniform(0, 1000), ndigits=3)}'
                                    for i in range(param)])
            problems.append(parse_problem(problem_str))
    return problems


def cost(state, other, problem):
    """Returns the cost of the operation of moving from one state to
    another.

    Cost is calculated by { . . . }

    Args:
        state: Parent state.
        other: Child state of Parent.
        problem: namedtuple instance representing problem.

    Returns:
        The integer cost of moving from state to other.
    """
    for i, x in enumerate(state.state):
        if x.visited == 0:
            for j, y in enumerate(other.state):
                if y.visited == 0:
                    return _dist(x.point, y.point)

def _get_epsilon(cities):
    """Returns the minimum edge weight between any two cities in a
    provided list.

    Args:
        cities: A list of City objects.

    Returns:
        An integer value for the smallest edge cost.
    """
    return min(_dist(city_1, city_2) for city_1, city_2 in product(cities, cities) if city_1 != city_2)

def _dist(city_1: City, city_2: City):
    """Gives the euclidean distance between two cities, rounded up.

    Args:
        city_1, city_2: An object of type City.

    Returns:
        Integer value.
    """
    out = math.ceil(math.sqrt((city_1.x - city_2.x)**2 + (city_1.y - city_2.y)**2))
    return out


def _min_edge_in(city, cities):
    return min(_dist(city, other) for other in cities if other != city)


def edges_in_heuristic_fw(state, goal, degradation, problem):
    direction = -1
    h = 0
    for city, visited in state.state:
        if visited == direction:
            h += _min_edge_in(city, cities=problem.statics[0])
    return h


def edges_in_heuristic_bw(state, goal, degradation, problem):
    direction = 1
    h = 0
    for city, visited in state.state:
        if visited == direction:
            h += _min_edge_in(city, cities=problem.statics[0])
    return h

def zero_heuristic(state, goal, degradation, problem):
    """Zero heuristic function.

    Args:
        state: A state of {domain name} domain.
        goal: A state of {domain name} domain.
        degradation: Unused.
        problem: Unused.

    Returns:
        Integer value 0
    """
    return 0


# format: "heuristic_name": (forward_h, forward_h, backward_h)
heuristics = {"zero": (zero_heuristic,
                       zero_heuristic),
              "edges_in": (edges_in_heuristic_fw,
                           edges_in_heuristic_bw)
}
