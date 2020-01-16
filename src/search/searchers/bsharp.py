# bsharp.py

__name__ = 'bsharp'
__all__ = ['BSharpSearch']

import functools
from math import inf
import sys
import time

from src.search.utils import datastructures as ds


class BSharpSearch:
    def __init__(self, domain, heuristics, degradation, search_settings):
        self.domain = domain
        self.heuristic_fw = functools.partial(heuristics[1], degradation=degradation)
        self.heuristic_bw = functools.partial(heuristics[2], degradation=degradation)
        self.initial = None
        self.goal = None
        self.epsilon = None
        self.split = search_settings['split']
        self.best = inf
        self.collision_nodes = (None, None)
        self.gLim = {1: 0,
                     -1: 0}
        self.fLim = 0

        self.openlist = {
            1 : ds.OpenList(),  # forward
            -1 : ds.OpenList()  # backward
            }
        self.closedlist = {
            1: ds.ClosedList(),
            -1: ds.ClosedList()
        }

        self.settings = search_settings

        self.nodes_expanded = 0
        self.nodes_generated = 2
        self.started_0_expansion = {-1: set(), 1: set()}
        self.expanded_this_layer = {-1: set(), 1: set()}
        self.removed = set()

    def bsharp(self):
        self.initial, self.goal = self.problem.initial, self.problem.goal
        self.epsilon = self.problem.epsilon

        self.openlist[1].append(ds.Node(
            state=self.initial,
            g=0,
            h=self.heuristic_fw(self.initial),
            direction=1
        ))

        self.openlist[-1].append(ds.Node(
            state=self.goal,
            g=0,
            h=self.heuristic_bw(self.goal),
            direction=-1
        ))

        self.fLim = max(self.heuristic_fw(self.initial),
                        self.heuristic_bw(self.goal),
                        self.epsilon)

        while len(self.openlist[1]) != 0 and len(self.openlist[-1]) != 0:
            if self.best == self.fLim:
                return

            self.split_fn(self.fLim - self.epsilon + 1)
            self.expanded_this_layer = {-1: set(), 1: set()}
            self.expand_level()
            # print(self.fLim, self.gLim, len(self.expanded_this_layer[-1]), len(self.expanded_this_layer[1]))
            if self.best == self.fLim:
                return

            self.fLim += 1
        return

    def expand_level(self):
        expandable = self.get_expandable_nodes()
        while len(expandable) != 0:
            n = expandable.pop()
            dir = n.direction

            if n.n_expanded == 0 and not n.expanded_nonce:
                self.started_0_expansion[dir].add(n.state.state)
                self.expanded_this_layer[dir].add(n.state.state)
                n.expanded_nonce = True

            for child_state, child_g in self.expand(n):
                if child_state in self.closedlist[dir]:
                    continue
                elif child_state in self.openlist[dir]:
                    prev_c_g = self.openlist[dir].get_g(child_state)
                    if child_g >= prev_c_g:
                        continue

                child_node = self.generate_child(child_state, parent=n)
                if child_node.g < self.gLim[dir] and child_node.f <= self.fLim:
                    expandable.add(child_node)

                if child_node in self.openlist[-1 * dir]:  # opposite openlist
                    old_best = self.best
                    self.best = min(self.best, child_node.g + self.openlist[-1 * dir].get_g(child_state))
                    if self.best != old_best:
                        self.collision_nodes = (self.openlist[1].get(child_state), self.openlist[-1].get(child_state))
                    if self.best <= self.fLim:
                        return

            if n.is_fully_expanded():
                self.openlist[dir].remove(n)
                self.closedlist[dir].append(n)
                self.nodes_expanded += 1
        return

    def generate_child(self, child_state, parent):
        temp_g = parent.g + self.domain.cost(parent.state, child_state, problem=self.problem)
        dir = parent.direction
        if child_state in self.openlist[dir]:
            self.openlist[dir].remove(child_state)
        if child_state in self.closedlist[dir]:
            self.closedlist[dir].remove(child_state)

        c_node = ds.Node(
            state=child_state,
            g=temp_g,
            h=self.heuristic_fw(child_state) if dir == 1 else self.heuristic_bw(child_state),
            direction=parent.direction,
            parent=parent
        )

        self.nodes_generated += 1
        self.openlist[dir].append(c_node)
        return c_node

    def get_expandable_nodes(self):
        expandable_f = {node for node in self.openlist[1]
                        if node.f <= self.fLim and node.g < self.gLim[1]}
        expandable_b = {node for node in self.openlist[-1]
                        if node.f <= self.fLim and node.g < self.gLim[-1]}
        expandable = expandable_f.union(expandable_b)
        return expandable

    def goal_test(self, state, goal):
        return state == goal

    def split_fn(self, gLSum):
        while self.gLim[-1] + self.gLim[1] != gLSum:
            if self.gLim[1] / gLSum < self.split:
                self.gLim[1] += 1
            else:
                self.gLim[-1] += 1
        return

    def expand(self, node):
        self.openlist[node.direction].remove(node)
        self.closedlist[node.direction].append(node)
        self.nodes_expanded += 1
        return ((s, c) for s, c in node.expand(problem=self.problem))

    def write_out(self, label):
        solution_path = f'{self.collision_nodes[0].path()[:-1]} ' \
                        f'+ {self.collision_nodes[0].state.state} ' \
                        f'+ {self.collision_nodes[1].path(reverse=True)[1:]}'
        original_std = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}.out', 'w')
        print(f'Problem = {self.problem.initial}\n'
              f'Expanded = {self.nodes_expanded}\n'
              f'Tried expanding = {len(self.started_0_expansion[1]) + len(self.started_0_expansion[-1])}\n'
              f'Generated = {self.nodes_generated}\n'
              f'Open list size at end (fw) = {len(self.openlist[1])}\n'
              f'Open list size at end (bw) = {len(self.openlist[-1])}\n'
              f'Closed list size at end (fw) = {len(self.closedlist[1])}\n'
              f'Closed list size at end (bw) = {len(self.closedlist[-1])}\n'
              f'Solution length = {self.best}\n'
              f'Solution path = {solution_path}\n'
              f'Heuristic = {self.heuristic_fw}')
        sys.stdout = original_std

    def __call__(self, problem, label):
        self.problem = problem
        self.heuristic_fw = functools.partial(self.heuristic_fw, goal=problem.goal, problem=problem)
        self.heuristic_bw = functools.partial(self.heuristic_bw, goal=problem.initial, problem=problem)

        print('Starting bsharp')
        since = time.perf_counter()
        self.bsharp()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)
