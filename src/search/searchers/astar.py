# astar.py

__name__ = 'astar'
__all__ = ['AStarSearch', 'astar']

import functools
import math
import sys
import time

from src.search.utils import datastructures as ds


class AStarSearch:
    def __init__(self, domain, heuristics, degradation, search_settings):
        self.domain = domain
        self.openlist = ds.OpenList()
        self.closedlist = ds.ClosedList()
        self.problem = None
        self.goal_node = None
        self.best = math.inf

        self.heuristic = functools.partial(heuristics[0], degradation=degradation)
        self.h_weighting = search_settings.get('heuristic_weighting', 1)

        self.nodes_generated = 1
        self.nodes_expanded = 0

    def astar(self):
        initial, goal = self.problem.initial, self.problem.goal
        self.openlist.append(
            ds.Node(state=initial, g=0, h=(self.heuristic(initial) * self.h_weighting)))

        while len(self.openlist) > 0:
            node = self.openlist.peek()
            if self.goal_test(node.state, goal):
                self.goal_node = node
                self.best = node.g
                return

            children = self.expand(node)
            for child, _ in children:
                if child in self.closedlist:
                    continue
                self.generate_child(child, parent=node)
        return

    def generate_child(self, child, parent):
        temp_g = parent.g + self.domain.cost(parent.state, child, problem=self.problem)
        if child in self.openlist and temp_g < self.openlist.get_g(child):
            self.openlist.replace(child, ds.Node(
                state=child,
                g=temp_g,
                h=(self.heuristic(child) * self.h_weighting),
                parent=parent))
        else:
            self.openlist.append(ds.Node(
                state=child,
                g=temp_g,
                h=(self.heuristic(child) * self.h_weighting),
                parent=parent))
        self.nodes_generated += 1

    def expand(self, node):
        self.openlist.remove(node)
        self.closedlist.append(node)
        self.nodes_expanded += 1
        return (s for s in node.expand(problem=self.problem))

    def goal_test(self, state, goal):
        return state == goal

    def write_out(self, label):
        original_std = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}.out', 'w')
        print(f'Expanded = {self.nodes_expanded}\n'
              f'Generated = {self.nodes_generated}\n'
              f'Solution length = {self.best}\n'
              f'Open list size at end = {len(self.openlist)}\n'
              f'Closed list size at end = {len(self.closedlist)}\n'
              f'Expansion = {self.expand}\n'
              f'Weighting = {self.h_weighting}')
        sys.stdout = original_std

    def __call__(self, problem, label):
        self.problem = problem
        self.heuristic = functools.partial(self.heuristic, goal=problem.goal, problem=problem)
        since = time.perf_counter()
        self.astar()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)

