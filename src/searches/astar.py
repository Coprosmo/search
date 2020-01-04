# astar.py

from math import inf
from ..utils import datastructures as ds
__name__ = 'astar'

print('Loading astar.py...')


def search(problem, domain):
    openlist = ds.OpenList()
    closedlist = ds.ClosedList()
    initial, goal = problem['initial'], problem['goal']
    openlist.append(
        ds.Node(
            state=initial,
            g=0,
            h=domain.heuristic(initial)))

    while len(openlist) > 0:
        node = openlist.pop()
        closedlist.append(node)
        print(f"Expanding node: g={node.g}, f={node.f}")

        if domain.goal_test(node.state, goal):
            print("Solution found")
            solution = node.path()
            return solution, node.g

        children = node.expand()
        for child in children:
            if child in closedlist:
                continue

            temp_g = node.g + domain.cost(node.state, child.state)
            if child in openlist and temp_g < openlist.get_g(child):
                openlist.replace(child,
                                 ds.Node(
                                    state=child.state,
                                    g=temp_g,
                                    h=domain.heuristic(child.state)))

    print('No solution found')
    return inf


def _setup_vars(problem):
    raise NotImplementedError