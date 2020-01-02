__all__ = ['Node']


class Node:
    def __init__(self, state, g, h=0):
        """Domain/search-independent node structure, contains state info, as well as g, [h, f] values."""
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h