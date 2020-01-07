from collections import namedtuple
from math import inf
import heapq

from .node import Node

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

    def get_g(self, state):
        for other in self.openlist:
            if other.state == state:
                return other.g
        return inf

    def get(self, node):
        if isinstance(node, Node):
            state = node.state
        else:
            state = node

        for other in self.openlist:
            print(other.state, state)
            if other.state == state:
                return other
        raise Exception("Node not found.")

    def replace(self, node, other):
        if isinstance(node, Node):
            state = node.state
        else:
            state = node

        for i, x in enumerate(self.openlist):
            if x.state == state:
                self.openlist[i] = other
                return

        raise Exception("Node not found.")

    def remove(self, node):
        if isinstance(node, Node):
            state = node.state
        else:
            state = node

        for i in range(len(self.openlist)):
            if self.openlist[i].state == state:
                break
        self.openlist.pop(i)

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
        return self.openlist[item]

    def __contains__(self, obj):
        if isinstance(obj, Node):
            state = obj.state
            return any([other.state == state for other in self.openlist])
        else:
            return any([other.state == obj for other in self.openlist])
