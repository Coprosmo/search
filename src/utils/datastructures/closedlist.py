from .node import Node

__all__ = ['ClosedList']


class ClosedList:
    def __init__(self):
        self.closedlist = set()

    def append(self, node):
        self.closedlist.add(node.state)

    def remove(self, node):
        if isinstance(node, Node):
            state = node.state
        else:
            state = node
        self.closedlist.remove(state)

    def __len__(self):
        return len(self.closedlist)

    def __contains__(self, obj):
        if isinstance(obj, Node):
            state = obj.state
            return state in self.closedlist
        else:
            return obj in self.closedlist

    def __iter__(self):
        return iter(self.closedlist)

