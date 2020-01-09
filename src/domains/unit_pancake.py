# unit_pancake.py

from collections import namedtuple
from random import sample

from .domain_template import DomainTemplate


Problem = namedtuple('Problem', 'initial goal epsilon')

Problem.__defaults__ = (1,)


def parse_problem(problem_str):
    initial_tuple = tuple(map(int, problem_str.split(' ')))
    goal_tuple = tuple(range(len(initial_tuple), 0, -1))
    problem = Problem(initial=State(initial_tuple),
                      goal=State(goal_tuple),
                      epsilon=1)
    return problem


def pancake_predicates(pancake_stack):
    state = set()
    state.add(('on', pancake_stack[-1], None))
    state.add(('on', None, pancake_stack[0]))
    for i in range(len(pancake_stack) - 1, 0, -1):
        state.add(('on', pancake_stack[i - 1], pancake_stack[i]))
    state = frozenset(state)
    return state


def generate_problems(config):
    problems = []
    if config.settings['precompiled']:
        for file_name in config.settings['precompiled']:
            with open(file_name, 'r') as f:
                problems.append(parse_problem(f.readline()))
    else:
        pass
    return problems


class State:
    def __init__(self, state):
        self.state = state

    def successors(self):
        output = []
        for i in range(1, len(self.state)):
            first = [self.state[j] for j in range(i)]
            second = [self.state[j] for j in range(len(self.state)-1, i-1, -1)]
            output.append(State(tuple(first + second)))
        return output

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        return self.SuccessorIter(self.state)

    def __repr__(self):
        return f'State(state={self.state})'

    def __eq__(self, other):
        return self.state == other.state

    class SuccessorIter:
        def __init__(self, state):
            self.state = state
            self.i = 1

        def __iter__(self):
            return self

        def __next__(self):
            return State(self.state[:self.i:-1] + self.state[self.i::])


def successors(state):
    output = []
    for i in range(1, len(state) + 1):
        output.append(State(state[:i:-1] + state[i::]))
    return output


def heuristic(state, goal):
    return NotImplementedError


def gap_heuristic_fw(state, goal):
    print(heuristic.degradation)
    s, g = state.state, goal.state
    h = sum([int(bool(_adjacent(s[i], s[i+1], g))) for i in range(len(g) - 1)])
    return h


def gap_heuristic_bw(state, goal):
    return gap_heuristic_fw(state, goal)


def zero_heuristic(state, goal):
    return 0

def cost(state, other):
    return 1


def _adjacent(p1, p2, state):
    adj = True
    for i in range(len(state) - 1):
        pair = (state[i], state[i+1])
        if p1 in pair and p2 in pair:
            adj = False
    return adj


heuristics = {"zero" : (zero_heuristic, zero_heuristic, zero_heuristic),
              "gap" : (gap_heuristic_fw, gap_heuristic_fw, gap_heuristic_bw)}


