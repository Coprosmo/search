
__all__ = ['Node']

class Node:
    def __init__(self, state, g, h=0, parent=None, action=None):
        """Domain/search-independent node structure, contains state info, as well as g, [h, f] values."""
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.action = action

    def expand(self):
        raise NotImplementedError

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return tuple(reversed(path_back))

    def __repr__(self):
        return f'<Node(g = {self.g}, f = {self.f})>'

    def __str__(self):
        return f'<Node(g = {self.g}, f = {self.f})>'

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __gt__(self, other):
        return self.f > other.f

    def __ge__(self, other):
        return self.f >= other.f

    def __eq__(self, other):
        return self.state == other.state
