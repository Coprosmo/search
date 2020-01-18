"""A* Search"implementation.

Search is represented by a callable class which is instantiated with
desired settings.

There is an optional argument specifiable in a passed config file which
allows for running weighted A* experiments.

Typical usage:

    searcher = AStarSearch(unit_pancake, gap_heuristic, 0, search_settings)
    searcher(my_problem, "my_search")
"""

__name__ = 'astar'
__all__ = ['AStarSearch', 'astar']

import functools
import math
import sys
import time

from src.search.utils import datastructures as ds


class AStarSearch:
    """AStarSearch allows for the dynamic creation of easily
    configurable A* searchers, which can be called to run on specified
    problems.

    Attributes:
        domain: The module reference for the domain being used.
        openlist: OpenList structure containing nodes which have been
            generated but not yet fully expanded.
        closedlist: ClosedList structure containing states which have
            been generated and fully expanded.
        problem: An instance of namedtuple representing a search problem
        goal_node: Node on which a solution is found (initially None)
        best: Best solution cost found so far
        heuristic: Heuristic function to use during search
        h_weighting: (Optional) variable used for running weighted A*
    """
    def __init__(self, domain, heuristics, degradation, search_settings):
        """Initializing search object"""
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
        """Main flow control for A* search."""
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
        """Generates a child node, including heuristic and f-values,
        given a state and parent node. Inserts generated node into open
        list.

        Args:
            child: A state object, whose corresponding node is to be
                generated.
            parent: A node object, predecessor of child state.
        """
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
        """Gets children states of a specified node. Removes parent
        node from open-list if fully expanded, and inserts into
        closed list.

        Args:
            node: Node object to be expanded.

        Returns:
            A generator expression for the children of node.
        """
        self.openlist.remove(node)
        self.closedlist.append(node)
        self.nodes_expanded += 1
        return (s for s in node.expand(problem=self.problem))

    def goal_test(self, state, goal):
        """Tests whether a state is a goal.

        Args:
            state: State object to test as a goal
            goal: State object representing the goal

        Returns:
            A boolean value as to whether state is a goal.
        """
        return state == goal

    def write_out(self, label):
        """Writes specific statistics about search to a file.

        Args:
            label: A string containing the name of the file to write to.
        """
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
        """Runs an instance of AStarSearch.

        Callable method accessed by calling an instance of this class.

        Args:
            problem: A namedtuple representing the problem instance to
                run.
            label: String containing the name of the file to write
                statistics to.
        """
        self.problem = problem
        self.heuristic = functools.partial(self.heuristic, goal=problem.goal, problem=problem)
        since = time.perf_counter()
        self.astar()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)
