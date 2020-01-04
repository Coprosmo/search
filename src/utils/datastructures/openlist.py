from collections import namedtuple
from math import inf
import heapq

__all__ = ['OpenList']


class OpenList:
    """Standard open list implementation"""
    def __init__(self):
        self.openlist = []

    def append(self, node):
        heapq.heappush(self.openlist, node)

    def pop(self):
        out = heapq.heappop(self.openlist)
        return out

    def get_g(self, node):
        for other in self.openlist:
            if other.state == node.state:
                return other.g
        return inf

    def get(self, state):
        for other in self.openlist:
            if other.state == state:
                return other
        raise Exception("Node not found.")

    def replace(self, node, other):
        for i, x in enumerate(self.openlist):
            if x == node:
                self.openlist[i] = other
        raise Exception("Node not found.")

    def __repr__(self):
        return str(self.openlist)

    def __str__(self):
        out = f"""Size: {len(self.openlist)}
g values: (min: {self.min_g}, max: {self.max_g})
f values: (min: {self.min_f}, max: {self.max_f})"""
        return out

    def __len__(self):
        return len(self.openlist)

    def __getitem__(self, item):
        return heapq.nsmallest(item, self.openlist)[-1]

    def __contains__(self, node):
        state = node.state
        return any([other.state == state for other in self.openlist])
