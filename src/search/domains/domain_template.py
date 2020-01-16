"""{domain name} domain.

Typical use:

    state_1 = {domain_name}.State( . . . )
    state_2 = {domain_name}.State( . . . )
    h = {domain_name}.cost(state_1, state_2, *problem variable*)
"""

from collections import namedtuple
import math
import random


Problem = namedtuple('Problem', 'initial goal epsilon')


class State:
    """State class specific to {domain name} domain.

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
        self.n_successors = NotImplemented
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
            """ Get successor states, costs and append as (state, cost) to self.successors_list """
            self.successors_list = sorted(self.successors_list, key=lambda x: x[1])
        return self.successors_list

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f'State({self.state})'

    def __eq__(self, other):
        raise NotImplementedError


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
    initial_tuple = NotImplemented
    goal_tuple = NotImplemented
    epsilon = NotImplemented
    problem = Problem(initial=State(initial_tuple),
                      goal=State(goal_tuple),
                      epsilon=epsilon)
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
            """Generate problem and append to problems"""

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
    raise NotImplementedError


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
                       zero_heuristic,
                       zero_heuristic)}
