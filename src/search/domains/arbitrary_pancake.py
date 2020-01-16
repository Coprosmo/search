"""Arbitrary-cost pancake domain.

Typical use:

    state_1 = arbitrary_pancake.State( . . . )
    state_2 = arbitrary_pancake.State( . . . )
    h = arbitrary_pancake.cost(state_1, state_2, *problem variable*)
"""

from collections import namedtuple
import math
import random


Problem = namedtuple('Problem', 'initial goal epsilon')

Problem.__defaults__ = (1,)


class State:
    """State class specific to arbitrary-cost pancake domain.

    Includes successor function, as well as hash and equality
    __methods.

    Attributes:
        state: Immutable variable containing the state description.
        n_successors: Number of successors of the state.
        successors_list: Lazily-calculated list of (state, cost)
            tuples, as the successors of self.
    """

    def __init__(self, state):
        """Initializes State object."""
        self.state = state
        self.n_successors = len(self.state) - 2
        self.successors_list = None

    def successors(self, problem):
        """Get successors of self, sorted by cost.

        Lazily calculates the successors. If function hasn't been
        called before, successors are calculated and stored.
        If stored list exists, it is simply retrieved.

        Args:
            problem: namedtuple object as created in parse_problem().

        Returns:
            A sorted list of the successors of self.
        """
        if self.successors_list is None:
            self.successors_list = []
            for i in range(len(self.state) - 2, 0, -1):
                first = [self.state[j] for j in range(i)]
                second = [self.state[j] for j in range(len(self.state)-1, i-1, -1)]
                new_state = State(tuple(first + second))
                self.successors_list.append((new_state, cost(self, new_state, problem=problem)))
            self.successors_list = sorted(self.successors_list, key=lambda x: x[1])
        return self.successors_list

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f'State(state={self.state})'

    def __eq__(self, other):
        return self.state == other.state


def parse_problem(problem_str):
    """Create namedtuple instance of specified problem.

    Creates a namedtuple instance containing various information about
    the problem, including initial state, goal state, and epsilon
    (minimum operator cost).

    Args:
        problem_str: A string representation of the problem, where
            pancake base is the leftmost character, and other
            pancakes are separated by spaces

            e.g. 6 4 3 2 1 5

                A stack of five pancakes, with '1' being the smallest,
                5 the largest, and 6 the base.

    Returns:
        A namedtuple containing problem information.
    """
    initial_tuple = tuple(map(int, problem_str.split(' ')))
    goal_tuple = tuple(range(len(initial_tuple), 0, -1))
    problem = Problem(initial=State(initial_tuple),
                      goal=State(goal_tuple),
                      epsilon=1)
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
        A list of namedtuple instances representing arbitrary-pancake
            problems.
    """
    problems = []
    if config.settings['precompiled']:
        for file_name in config.settings['precompiled']:
            with open(file_name, 'r') as f:
                for line in f:
                    problems.append(parse_problem(line))
    else:
        try:
            n_problems = config.settings['n_problems']
            param = config.settings['param']
        except KeyError:
            raise Exception("For config file specifying no precompiled problem, ensure parameters 'params', "
                            "'n_problems' are set'")
        for p in range(n_problems):
            x = [i for i in range(1, param)]
            random.shuffle(x)
            problem_str = ' '.join(map(str, [param] + x))
            problems.append(parse_problem(problem_str))

    return problems


def cost(state, other, problem):
    """Returns the cost of the operation of moving from one state to
    another.

    Cost is calculated by counting the number of pancakes flipped in
    the operation.

    Args:
        state: Parent state.
        other: Child state of Parent.
        problem: namedtuple instance representing problem.

    Returns:
        The integer cost of moving from state to other.
    """
    state_1, state_2 = state.state, other.state
    i = 0
    while state_1[i] == state_2[i] and i < len(state_1):
        i += 1
    return len(state_1) - i


def _not_adjacent(p1, p2, state):
    """Determines whether or not two pancakes are adjacent in a given
    state.

    Args:
        p1: First pancake.
        p2: Second pancake.
        state: State to check for adjacency.

    Returns:
        A boolean value.
    """
    adj = True
    for i in range(len(state) - 1):
        pair = (state[i], state[i+1])
        if p1 in pair and p2 in pair:
            adj = False
    return adj


def largest_pancake_heuristic_fw(state, goal, degradation, problem):
    """Forward direction 'Largest pancake' Heuristic function for the
    arbitrary-pancake domain.

    Heuristic is calculated to be the weight of the largest pancake
    which is out of place in a state, with respect to the goal state.

    Heuristic can be degraded by specifying an integer
    value 0 <= x <= 10, where 0 is perfect heuristic, and 10 is blind.
    Degradation involves ignoring the top (degradation / 10)% of the
    pancakes when calculating heuristic.

    Args:
        state: A state of arbitrary-pancake domain.
        goal: A state of arbitrary-pancake domain.
        degradation: An integer between 0 and 10 inclusive.
        problem: A namedtuple instance representing a arbitrary-pancake
            problem.

    Returns:
        A non-negative integer value for the heuristic value of state.
    """
    if state == goal:
        return 0
    stop_condition = len(goal.state) - math.floor((degradation / 10) * len(goal.state))
    return state.state[max(i for i in range(1, stop_condition) if state.state[i] != goal.state[i])]


def largest_pancake_heuristic_bw(state, goal, degradation, problem):
    """Backward direction 'Largest Pancake' Heuristic function for the
    arbitrary-pancake domain.

    Heuristic is calculated to be the weight of the largest pancake
    which is out of place in a state, with respect to the goal state.

    Heuristic can be degraded by specifying an integer
    value 0 <= x <= 10, where 0 is perfect heuristic, and 10 is blind.
    Degradation involves ignoring the top (degradation / 10)% of the
    pancakes when calculating heuristic.

    Args:
        state: A state of arbitrary-pancake domain.
        goal: A state of arbitrary-pancake domain.
        degradation: An integer between 0 and 10 inclusive.
        problem: A namedtuple instance representing a arbitrary-pancake
            problem.

    Returns:
        A non-negative integer value for the heuristic value of state.
    """
    return largest_pancake_heuristic_fw(state, goal)


def zero_heuristic(state, goal, degradation, problem):
    """Zero heuristic function.

    Args:
        state: A state of arbitrary-pancake domain.
        goal: A state of arbitrary-pancake domain.
        degradation: Unused.
        problem: Unused.

    Returns:
        Integer value 0
    """
    return 0


heuristics = {"zero": (zero_heuristic,
                       zero_heuristic,
                       zero_heuristic),
              "largest_pancake": (largest_pancake_heuristic_fw,
                                  largest_pancake_heuristic_fw,
                                  largest_pancake_heuristic_bw)}
