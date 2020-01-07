
__all__ = ['Node']

class Node:
    def __init__(self, state, g, h=0, direction=1, parent=None, action=None):
        """Domain/search-independent node structure, contains state info, as well as g, [h, f] values."""
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.direction = direction
        self.parent = parent
        self.action = action
        self.depth = parent.depth + 1 if parent else 0

    def expand(self):
        return self.state.successors()

    def path(self, reverse=True):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        if reverse:
            out = tuple(reversed(path_back))
        else:
            out = tuple(path_back)
        return out

    def __hash__(self):
        return hash((self.state, self.g, self.f, self.direction, self.parent))

    def __repr__(self):
        return f'Node(g={self.g}, f={self.f}, state={self.state})'

    def __str__(self):
        return f'Node(g={self.g}, f={self.f}, state={self.state})'

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
