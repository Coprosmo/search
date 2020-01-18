"""B# Search implementation.

Search is represented by a callable class which is instantiated with
desired settings.

Typical usage:

    searcher = BSharpSearch(unit_pancake, gap_heuristic, 0, search_settings)
    searcher(my_problem, "my_search")
"""

__name__ = 'bsharp'
__all__ = ['BSharpSearch']

import functools
from math import inf
import sys
import time

from src.search.utils import datastructures as ds


class BSharpSearch:
    """BSharpSearch allows for the dynamic creation of easily
    configurable B# searchers, which can be called to run on specified
    problems.

    Attributes:
        domain: The module reference for the domain being used.
        openlist: OpenList structure containing nodes which have been
            generated but not yet fully expanded.
        closedlist: ClosedList structure containing states which have
            been generated and fully expanded.
        initial: Initial state of search
        goal: Goal state of search
        epsilon: Cost of cheapest operator in domain
        split: Between 0 and 1, defines the split of gLims
        gLim: Maximum g-value from which nodes can no longer be expanded
        fLim: Maximum f-value from which nodes can no longer be expanded
        goal_node: Node on which a solution is found (initially None)
        best: Best solution cost found so far
        heuristic_fw: Forward heuristic function to use during search
        heuristic_bw: Backward heuristic function to use during search
    """

    def __init__(self, domain, heuristics, degradation, search_settings):
        """Initializes search object"""
        self.domain = domain
        self.heuristic_fw = functools.partial(heuristics[1], degradation=degradation)
        self.heuristic_bw = functools.partial(heuristics[2], degradation=degradation)
        self.initial = None
        self.goal = None
        self.epsilon = None
        self.split = search_settings['split']

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

        self.best = inf
        self.collision_nodes = (None, None)
        self.settings = search_settings
        self.nodes_expanded = 0
        self.nodes_generated = 2
        self.started_0_expansion = {-1: set(), 1: set()}
        self.expanded_this_layer = {-1: set(), 1: set()}

    def bsharp(self):
        """Main flow control for B# search"""
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
        """Expands all expandable nodes at the current fLim.

        Expandable nodes are those with g < gLim, and f <= fLim.
        """
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
        """Generates a child node, including heuristic and f-values,
        given a state and parent node. Inserts generated node into open
        list.

        Args:
            child: A state object, whose corresponding node is to be
                generated.
            parent: A node object, predecessor of child state.
        """
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
        """Gets all nodes expandable nodes with the current fLIM and
        gLim.

        Returns:
            A set containing all expandable nodes from either openlist.
        """
        expandable_f = {node for node in self.openlist[1]
                        if node.f <= self.fLim and node.g < self.gLim[1]}
        expandable_b = {node for node in self.openlist[-1]
                        if node.f <= self.fLim and node.g < self.gLim[-1]}
        expandable = expandable_f.union(expandable_b)
        return expandable

    def goal_test(self, state, goal):
        """Tests whether a state is a goal.

        Args:
            state: State object to test as a goal
            goal: State object representing the goal

        Returns:
            A boolean value as to whether state is a goal.
        """
        return state == goal

    def split_fn(self, gLSum):
        """Determines the gLim values (fw and bw) given the split ratio
        and current fLim.
        """
        while self.gLim[-1] + self.gLim[1] != gLSum:
            if self.gLim[1] / gLSum < self.split:
                self.gLim[1] += 1
            else:
                self.gLim[-1] += 1
        return

    def expand(self, node):
        """Gets children states of a specified node. Removes parent
        node from open-list if fully expanded, and inserts into
        closed list.

        Args:
            node: Node object to be expanded.

        Returns:
            A generator expression for the children of node.
        """
        self.openlist[node.direction].remove(node)
        self.closedlist[node.direction].append(node)
        self.nodes_expanded += 1
        return ((s, c) for s, c in node.expand(problem=self.problem))

    def write_out(self, label):
        """Writes specific statistics about search to a file.

        Args:
            label: A string containing the name of the file to write to.
        """
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
        """Runs an instance of BSharpSearch.

        Callable method accessed by calling an instance of this class.

        Args:
            problem: A namedtuple representing the problem instance to
                run.
            label: String containing the name of the file to write
                statistics to.
        """
        self.problem = problem
        self.heuristic_fw = functools.partial(self.heuristic_fw, goal=problem.goal, problem=problem)
        self.heuristic_bw = functools.partial(self.heuristic_bw, goal=problem.initial, problem=problem)

        print('Starting bsharp')
        since = time.perf_counter()
        self.bsharp()
        now = time.perf_counter()
        print(f'All done! ({(now - since) // 60})m {(now - since) % 60}s')
        self.write_out(label)
