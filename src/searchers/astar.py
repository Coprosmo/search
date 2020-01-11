# astar.py

__name__ = 'astar'
__all__ = ['AStarSearch', 'astar']

import functools
import sys
import time

from src.utils import datastructures as ds


class AStarSearch:
    def __init__(self, domain, heuristics, degradation, search_settings):
        self.domain = domain
        self.openlist = ds.OpenList()
        self.closedlist = ds.ClosedList()
        self.problem = None

        self.heuristic = functools.partial(heuristics[0], d=degradation)
        self.h_weighting = search_settings.get('heuristic_weighting', 1)

        # If user specifies an expansion protocol, try to use that, otherwise use standard protocol
        expansion_protocol = search_settings.get('expansion', None)
        self.expand = (expansion_protocol and getattr(AStarSearch, 'expand_' + search_settings['expansion'], 0)) \
            or self.expand_standard
        self.nodes_generated = 1
        self.nodes_expanded = 0

    def astar(self):
        initial, goal = self.problem.initial, self.problem.goal
        self.openlist.append(
            ds.Node(state=initial, g=0, h=(self.heuristic(initial) * self.h_weighting)))

        while len(self.openlist) > 0:
            node = self.openlist.peek()
            print(node.f)
            if self.goal_test(node.state, goal):
                return node

            children = self.expand(node)
            for child in children:
                if child in self.closedlist:
                    continue
                self.generate_child(child, parent=node)
        return

    def generate_child(self, child, parent):
        temp_g = parent.g + self.domain.cost(parent.state, child)
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

    def expand_standard(self, node):
        self.openlist.remove(node)
        self.closedlist.append(node)
        self.nodes_expanded += 1
        return (s for s in node.expand())

    def goal_test(self, state, goal):
        return state == goal

    def write_out(self, label):
        original_std = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}.out', 'w')
        print(f'Expanded = {self.nodes_expanded}\n'
              f'Generated = {self.nodes_generated}\n'
              f'Open list size at end = {len(self.openlist)}\n'
              f'Closed list size at end = {len(self.closedlist)}\n'
              f'Expansion = {self.expand}\n'
              f'Weighting = {self.h_weighting}')
        sys.stdout = original_std

    def __call__(self, problem, label):
        self.problem = problem
        self.heuristic = functools.partial(self.heuristic, goal=problem.goal)
        since = time.perf_counter()
        self.astar()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)

