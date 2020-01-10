# astar.py

from math import inf
import time

from ..utils import datastructures as ds

__name__ = 'astar'
__all__ = ['AStarSearch', 'astar']

nodes_generated = 1
nodes_expanded = 0


def astar(problem, domain):
    global nodes_generated, nodes_expanded

    openlist = ds.OpenList()
    closedlist = ds.ClosedList()
    initial, goal = problem.initial, problem.goal
    openlist.append(
        ds.Node(
            state=initial,
            g=0,
            h=domain.heuristic(initial, goal)))

    while len(openlist) > 0:
        node = openlist.pop()
        closedlist.append(node)
        nodes_expanded += 1

        if goal_test(node.state, goal):
            print("Solution found")
            solution = node.path()
            print(solution)
            solution_node = node
            return locals()

        children = node.expand()
        for child in children:
            if child in closedlist:
                continue

            temp_g = node.g + domain.cost(node.state, child)
            if child in openlist and temp_g < openlist.get_g(child):
                openlist.replace(child,
                                 ds.Node(
                                    state=child,
                                    g=temp_g,
                                    h=domain.heuristic(child, goal),
                                    parent=node))
            else:
                openlist.append(ds.Node(
                        state=child,
                        g=temp_g,
                        h=domain.heuristic(child, goal),
                        parent=node))
            nodes_generated += 1
    return locals()


def goal_test(state, goal):
    return state == goal


def search(problem, domain, settings):
    since = time.perf_counter()
    search_vars = astar(problem, domain)
    now = time.perf_counter()
    print(f'All done! ({(now - since)//60})m {(now - since) % 60}s')
    print(f'Expanded = {nodes_expanded}\n'
          f'Generated = {nodes_generated}')
    return search_vars


class AStarSearch:
    def __init__(self, domain, search_settings):
        self.domain = domain
        self.openlist = ds.OpenList()
        self.closedlist = ds.ClosedList()
        self.nodes_generated = 1
        self.nodes_expanded = 0

    def search(self, problem, domain):
        since = time.perf_counter()
        astar(problem)
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        print(f'Expanded = {nodes_expanded}\n'
              f'Generated = {nodes_generated}')
        self.write_out()

    def goal_test(self, state, goal):
        return state == goal

    def write_out(self):
        print(f'Expanded = {self.nodes_expanded}\n'
              f'Generated = {self.nodes_generated}')

    def astar(self, problem):
        initial, goal = problem.initial, problem.goal
        self.openlist.append(
            ds.Node(
                state=initial,
                g=0,
                h=self.domain.heuristic(initial, goal)))

        while len(self.openlist) > 0:
            node = self.openlist.pop()
            self.closedlist.append(node)
            self.nodes_expanded += 1

            if goal_test(node.state, goal):
                print("Solution found")
                solution = node.path()
                print(solution)
                solution_node = node
                return locals()

            children = node.expand()
            for child in children:
                if child in self.closedlist:
                    continue

                temp_g = node.g + self.domain.cost(node.state, child)
                if child in self.openlist and temp_g < self.openlist.get_g(child):
                    self.openlist.replace(child, ds.Node(
                                                     state=child,
                                                     g=temp_g,
                                                     h=self.domain.heuristic(child, goal),
                                                     parent=node))

                else:
                    self.openlist.append(ds.Node(
                        state=child,
                        g=temp_g,
                        h=self.domain.heuristic(child, goal),
                        parent=node))
                self.nodes_generated += 1
