# domainparser.py
import pddlpy

__all__ = ['DomainParser']

class DomainParser:
    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem
        self.domprob = pddlpy.DomainProblem(domain, problem)
        self.initial = self.domprob.initialstate()
        self.goal = self.domprob.goals()
        self.operators = self._get_operators(self.domprob)

    def successors(self, state):
        raise NotImplementedError


    def _get_operators(self, domprob):
        raise NotImplementedError