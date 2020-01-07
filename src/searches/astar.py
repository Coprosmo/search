# astar.py

from math import inf
import time

from ..utils import datastructures as ds
__name__ = 'astar'

print('Loading astar.py...')


def astar(problem, domain):
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
        print(f"Expanding node: g={node.g}, f={node.f}, state={node.state}")

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
    return locals()


def goal_test(state, goal):
    return state == goal


def search(problem, domain, settings):
    since = time.perf_counter()
    search_vars = astar(problem, domain)
    now = time.perf_counter()
    print(f'All done! ({(now - since)//60})m {(now - since) % 60}s')
    return search_vars
