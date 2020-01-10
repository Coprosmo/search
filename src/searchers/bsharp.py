# bsharp.py

from math import inf
import time

from ..utils import datastructures as ds

__name__ = 'bsharp'
__all__ = ['bsharp']

nodes_expanded = 0
nodes_generated = 2


def bsharp(problem, domain, settings):
    initial = problem.initial
    goal = problem.goal
    best = inf
    gLim = {1 : 0,
            -1 : 0}

    if goal_test(initial, goal):
        best = 0
        return locals()

    openlist = {
        1 : ds.OpenList(),  # forward
        -1 : ds.OpenList()  # backward
    }
    closedlist = {
        1 : ds.ClosedList(),
        -1 : ds.ClosedList()
    }

    openlist[1].append(ds.Node(
        state=initial,
        g=0,
        h=domain.heuristic_fw(initial, goal),
        direction=1
    ))
    openlist[-1].append(ds.Node(
        state=goal,
        g=0,
        h=domain.heuristic_bw(goal, initial),
        direction=-1
    ))

    fLim = max(domain.heuristic_fw(initial, goal),
               domain.heuristic_bw(goal, initial),
               problem.epsilon)

    while len(openlist[1]) != 0 and len(openlist[-1]) != 0:
        if best == fLim:
            return locals()

        gLim = split(gLim, fLim - problem.epsilon + 1, split=settings['split'])
        best = expand_level(openlist=openlist,
                     closedlist=closedlist,
                     gLim=gLim,
                     fLim=fLim,
                     best=best,
                     epsilon=problem.epsilon,
                     problem=problem,
                     domain=domain,
                     settings=settings)

        if best == fLim:
            return locals()

        fLim += 1
    return best


def expand_level(openlist, closedlist, gLim, fLim, best, epsilon, problem, domain, settings):
    global nodes_expanded, nodes_generated

    expandable_f = {node for node in openlist[1]
                        if node.f <= fLim and node.g < gLim[1]}
    expandable_b = {node for node in openlist[-1]
                        if node.f <= fLim and node.g < gLim[-1]}
    expandable = expandable_f.union(expandable_b)

    while len(expandable) != 0:
        n = expandable.pop()    # automatically removes n
        nodes_expanded += 1
        dir = n.direction
        openlist[dir].remove(n)
        closedlist[dir].append(n)

        for c in n.expand():
            temp_g = n.g + domain.cost(n.state, c)
            if c in closedlist[dir]:
                continue
            elif c in openlist[dir]:
                prev_c_g = openlist[dir].get_g(c)
                if temp_g >= prev_c_g:
                    continue

            if c in openlist[dir]:
                openlist[dir].remove(c)

            if c in closedlist[dir]:
                closedlist[dir].remove(c)

            c_node = ds.Node(
                state=c,
                g=temp_g,
                h=domain.heuristic_fw(c, problem.goal) if dir == 1 else domain.heuristic_bw(c, problem.initial),
                direction=n.direction,
                parent=n
            )
            nodes_generated += 1

            openlist[dir].append(c_node)
            if c_node.g < gLim[dir] and c_node.f <= fLim:
                expandable.add(c_node)

            if c_node in openlist[-1 * dir]:    # opposite openlist
                best = min(best, c_node.g + openlist[-1 * dir].get_g(c))
                if best <= fLim:
                    return best

    return best


def goal_test(state, goal):
    return state == goal


def split(gLim, gLSum, split):
    while gLim[-1] + gLim[1] != gLSum:
        if gLim[1] / gLSum < split:
            gLim[1] += 1
        else:
            gLim[-1] += 1
    return gLim


def search(problem, domain, settings):
    print('Starting bsharp')
    since = time.perf_counter()
    search_vars = bsharp(problem, domain, settings)
    now = time.perf_counter()
    print(f'All done! ({(now - since)//60})m {(now - since) % 60}s')
    print(f'Expanded = {nodes_expanded}\n'
          f'Generated = {nodes_generated}')
    return search_vars
