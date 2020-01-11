# astar.py

from math import inf
import time

from ..utils import datastructures as ds
import functools

__name__ = 'astar'
__all__ = ['AStarSearch', 'astar']

# nodes_generated = 1
# nodes_expanded = 0
#
#
# def astar(problem, domain):
#     global nodes_generated, nodes_expanded
#
#     openlist = ds.OpenList()
#     closedlist = ds.ClosedList()
#     initial, goal = problem.initial, problem.goal
#     openlist.append(
#         ds.Node(
#             state=initial,
#             g=0,
#             h=domain.heuristic(initial, goal)))
#
#     while len(openlist) > 0:
#         node = openlist.pop()
#         closedlist.append(node)
#         nodes_expanded += 1
#
#         if goal_test(node.state, goal):
#             print("Solution found")
#             solution = node.path()
#             print(solution)
#             solution_node = node
#             return locals()
#
#         children = node.expand()
#         for child in children:
#             if child in closedlist:
#                 continue
#
#             temp_g = node.g + domain.cost(node.state, child)
#             if child in openlist and temp_g < openlist.get_g(child):
#                 openlist.replace(child,
#                                  ds.Node(
#                                     state=child,
#                                     g=temp_g,
#                                     h=domain.heuristic(child, goal),
#                                     parent=node))
#             else:
#                 openlist.append(ds.Node(
#                         state=child,
#                         g=temp_g,
#                         h=domain.heuristic(child, goal),
#                         parent=node))
#             nodes_generated += 1
#     return locals()
#
#
# def goal_test(state, goal):
#     return state == goal
#
#
# def search(problem, domain, settings):
#     since = time.perf_counter()
#     search_vars = astar(problem, domain)
#     now = time.perf_counter()
#     print(f'All done! ({(now - since)//60})m {(now - since) % 60}s')
#     print(f'Expanded = {nodes_expanded}\n'
#           f'Generated = {nodes_generated}')
#     return search_vars


class AStarSearch:
    def __init__(self, domain, heuristics, degradation, search_settings):
        self.domain = domain
        self.openlist = ds.OpenList()
        self.closedlist = ds.ClosedList()
        self.problem = None

        self.heuristic = functools.partial(heuristics[0], d=degradation)
        # If user specifies an expansion protocol, try to use that, otherwise use standard protocol
        expansion_protocol = search_settings.get('expansion', 0)
        self.expand = (expansion_protocol and getattr(AStarSearch, 'expand_' + search_settings['expansion'], 0)) \
            or self.expand_standard
        self.nodes_generated = 1
        self.nodes_expanded = 0

    def astar(self):
        initial, goal = self.problem.initial, self.problem.goal
        self.openlist.append(
            ds.Node(state=initial, g=0, h=self.heuristic(initial, goal)))

        while len(self.openlist) > 0:
            node = self.openlist.peek()
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
                h=self.heuristic(child, self.problem.goal),
                parent=parent))
        else:
            self.openlist.append(ds.Node(
                state=child,
                g=temp_g,
                h=self.heuristic(child, self.problem.goal),
                parent=parent))
        self.nodes_generated += 1

    def expand_standard(self, node):
        self.openlist.remove(node)
        self.closedlist.append(node)
        self.nodes_expanded += 1
        return (s for s in node.expand())

    def goal_test(self, state, goal):
        return state == goal

    def write_out(self):
        print(f'Expanded = {self.nodes_expanded}\n'
              f'Generated = {self.nodes_generated}')

    def __call__(self, problem):
        self.problem = problem
        since = time.perf_counter()
        self.astar()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out()

