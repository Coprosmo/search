"""A template for the expected format of a domain to be used by package."""

from collections import namedtuple

State = namedtuple('State', 'predicate_1'
                            'predicate_2'
                            'predicate_3')

Problem = namedtuple('Problem', 'static_preds'
                                'initial'
                                'goal'
                                'epsilon')

Problem.__defaults__ = (1,)


class DomainTemplate:
    def __init__(self,
                 bidirectional: 'Domain to be used for bidirectional purposes' = False):

        if bidirectional:
            Heuristic = namedtuple('Heuristic', 'fw bw')
            self.heuristic = Heuristic(self.fw_heuristic, self.bw_heuristic)
        else:
            self.heuristic = self.fw_heuristic

    @staticmethod
    def generate_problem(config):
        raise NotImplementedError

    @staticmethod
    def successors(state):
        raise NotImplementedError

    @staticmethod
    def fw_heuristic(state):
        raise NotImplementedError

    @staticmethod
    def bw_heuristic(state):
        raise NotImplementedError

    @staticmethod
    def dist(state, other):
        raise NotImplementedError

    @staticmethod
    def _get_epsilon(problem):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError
