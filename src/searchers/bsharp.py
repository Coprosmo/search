# bsharp.py

__name__ = 'bsharp'
__all__ = ['BSharpSearch']

import functools
from math import inf
import sys
import time

from src.utils import datastructures as ds


class BSharpSearch:
    def __init__(self, domain, heuristics, degradation, search_settings):
        self.domain = domain
        self.heuristic_fw = functools.partial(heuristics[1], d=degradation)
        self.heuristic_bw = functools.partial(heuristics[2], d=degradation)
        self.initial = None
        self.goal = None
        self.epsilon = None
        self.split = search_settings['split']
        self.best = inf
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
        self.expand = getattr(BSharpSearch, 'expand_' + search_settings['expansion']) or self.expand_standard

        self.nodes_expanded = 0
        self.nodes_generated = 2

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
            self.expand_level()
            if self.best == self.fLim:
                return

            self.fLim += 1
        return

    def expand_level(self):
        expandable = self.get_expandable_nodes()
        while len(expandable) != 0:
            # TODO: Make this peek the node, not remove
            n = expandable.pop()  # automatically removes n
            self.nodes_expanded += 1
            dir = n.direction
            self.openlist[dir].remove(n)
            self.closedlist[dir].append(n)

            for c in self.expand(n):
                temp_g = n.g + self.domain.cost(n.state, c)
                if c in self.closedlist[dir]:
                    continue
                elif c in self.openlist[dir]:
                    prev_c_g = self.openlist[dir].get_g(c)
                    if temp_g >= prev_c_g:
                        continue

                c_node = self.generate_child(c, parent=n)
                if c_node.g < self.gLim[dir] and c_node.f <= self.fLim:
                    expandable.add(c_node)

                if c_node in self.openlist[-1 * dir]:  # opposite openlist
                    self.best = min(self.best, c_node.g + self.openlist[-1 * dir].get_g(c))
                    if self.best <= self.fLim:
                        return
        return

    def generate_child(self, c, parent):
        temp_g = parent.g + self.domain.cost(parent.state, c)
        dir = parent.direction
        if c in self.openlist[dir]:
            self.openlist[dir].remove(c)
        if c in self.closedlist[dir]:
            self.closedlist[dir].remove(c)

        c_node = ds.Node(
            state=c,
            g=temp_g,
            h=self.heuristic_fw(c) if dir == 1 else self.heuristic_bw(c),
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

    @staticmethod
    def expand_standard(node):
        return (s for s in node.expand())

    @staticmethod
    def expand_g_deferral(node):
        # TODO: Use filter() or generator with filter to get only states with g == G
        return (s for s in node.expand())

    def write_out(self, label):
        original_std = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}.out', 'w')
        print(f'Expanded = {self.nodes_expanded}\n'
              f'Generated = {self.nodes_generated}\n'
              f'Open list size at end (fw) = {len(self.openlist[1])}\n'
              f'Open list size at end (bw) = {len(self.openlist[-1])}\n'
              f'Closed list size at end (fw) = {len(self.closedlist[1])}\n'
              f'Closed list size at end (bw) = {len(self.closedlist[-1])}\n'
              f'Solution length = {self.best}\n'
              f'Expansion = {self.expand}')
        sys.stdout = original_std

    def __call__(self, problem, label):
        self.problem = problem
        self.heuristic_fw = functools.partial(self.heuristic_fw, goal=problem.goal)
        self.heuristic_bw = functools.partial(self.heuristic_bw, goal=problem.initial)

        print('Starting bsharp')
        since = time.perf_counter()
        self.bsharp()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)
