# unit_pancake.py

from collections import namedtuple
from random import sample
import math


Problem = namedtuple('Problem', 'initial goal epsilon')

Problem.__defaults__ = (1,)


def parse_problem(problem_str):
    initial_tuple = tuple(map(int, problem_str.split(' ')))
    goal_tuple = tuple(range(len(initial_tuple), 0, -1))
    problem = Problem(initial=State(initial_tuple),
                      goal=State(goal_tuple),
                      epsilon=1)
    return problem


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
        self.n_successors = len(self.state) - 2

    def successors(self):
        for i in range(len(self.state) - 2, 0, -1):
            first = [self.state[j] for j in range(i)]
            second = [self.state[j] for j in range(len(self.state)-1, i-1, -1)]
            new_state = State(tuple(first + second))
            yield new_state, cost(self, new_state)

        #     output.append(State(tuple(first + second)))
        # return output

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f'State(state={self.state})'

    def __eq__(self, other):
        return self.state == other.state


def successors(state):
    output = []
    for i in range(1, len(state) + 1):
        output.append(State(state[:i:-1] + state[i::]))
        new_state = State(state[:i:-1] + state[i::])
        yield new_state, cost(state, new_state)


def heuristic(state, goal, d):
    return NotImplementedError


def largest_pancake_heuristic_fw(state, goal, d):
    if state == goal:
        return 0
    stop_condition = len(goal.state) - math.floor((d / 10) * len(goal.state))
    return state.state[max(i for i in range(1, stop_condition) if state.state[i] != goal.state[i])]


def largest_pancake_heuristic_bw(state, goal, d):
    return largest_pancake_heuristic_fw(state, goal)


def zero_heuristic(state, goal, d):
    return 0


def cost(state, other):
    state_1, state_2 = state.state, other.state
    i = 0
    while state_1[i] == state_2[i] and i < len(state_1):
        i += 1
    return len(state_1) - i


def _adjacent(p1, p2, state):
    adj = True
    for i in range(len(state) - 1):
        pair = (state[i], state[i+1])
        if p1 in pair and p2 in pair:
            adj = False
    return adj


heuristics = {"zero" : (zero_heuristic, zero_heuristic, zero_heuristic),
              "largest_pancake" : (largest_pancake_heuristic_fw, largest_pancake_heuristic_fw, largest_pancake_heuristic_bw)}

if __name__ == "__main__":
    print(cost(State((5, 4, 1, 2, 3)), State((5, 4, 3, 2, 1))))


