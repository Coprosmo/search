# unit_pancake.py

from collections import namedtuple
from random import sample

from .domain_template import DomainTemplate

State = namedtuple('State', 'predicate_1'
                            'predicate_2'
                            'predicate_3')

Problem = namedtuple('Problem', 'static_preds'
                                'initial'
                                'goal'
                                'epsilon')

Problem.__defaults__ = (1,)


class Domain(DomainTemplate):

    @staticmethod
    def generate_problem(config):
        initial = sample(range(config.param), config.param)
        goal = range(config.param)
        static_preds = []
        problem = Problem(static_preds=static_preds,
                          initial=initial,
                          goal=goal
        )
        return problem

    @staticmethod
    def successors(state):
        pass

    @staticmethod
    def fw_heuristic(state):
        pass

    @staticmethod
    def bw_heuristic(state):
        pass

    @staticmethod
    def _get_epsilon(problem):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
