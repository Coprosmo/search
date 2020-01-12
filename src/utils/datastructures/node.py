"""Node module, for use in searching algorithms.

Typical use:
    my_node = Node(state, g=5, h=6)
    print(my_node.f)
      >> 11
"""

__all__ = ['Node']


class Node:
    """Node class for use in search.

    Attributes:
        state: An immutable object representing the state of the node.
        g: Cost of path leading from start -> current state.
        h: Heuristic value of state.
        f: f-value of node, equal to g + h.
        direction: Primarily for use in bidirectional search. Describes
            direction in which node was generated.
        parent: Node which precedes this node in path.
        action: Action used to get from parent to current node.
        depth: Number of steps in path to node.
        """

    def __init__(self, state, g, h=0, direction=1, parent=None, action=None):
        """Initializes Node object."""
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.G = self.g
        self.F = self.f
        self.direction = direction
        self.parent = parent
        self.action = action
        self.depth = parent.depth + 1 if parent else 0
        self.n_expanded = 0

    def expand(self, partial_expansion=False):
        """Expands node, to give all directly reachable children.

        Returns:
            A generator object for the successors of node's state.
        """
        if partial_expansion == "g":
            for i, (state, cost) in enumerate(self.state.successors()):
                if self.g + cost == self.G:
                    if i + 1 == self.state.n_successors:
                        self.G = None
                    yield state, cost
                elif self.g + cost > self.G:
                    self.G = self.g + cost
                    break
        else:
            for state, cost in self.state.successors():
                self.n_expanded += 1
                yield state, cost

    def path(self, reverse=True):
        """Gives the path from the initial state to node's state.

        Args:
            reverse: An optional argument. If false, returns path in
                reversed order.

        Returns:
            Tuple object containing the ordered path from initial
                state to current state. Contains node objects.
        """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        if reverse:
            out = tuple(reversed(path_back))
        else:
            out = tuple(path_back)
        return out

    def is_fully_expanded(self):
        """Returns a boolean value describing whether node has been
        fully expanded. Intended for use in deferred expansion search.

        Returns:
            A boolean value, True if node has been expanded, otherwise
                False.
        """
        return self.G is None

    def __hash__(self):
        """Gets hash value of node, based on state."""
        # return hash((self.state, self.g, self.f, self.direction, self.parent))
        return hash((self.state, self.direction))

    def __repr__(self):
        """Gives representation of node."""
        return f'Node(g={self.g}, f={self.f}, state={self.state})'

    def __str__(self):
        """Gives representation of node."""
        return f'Node(g={self.g}, f={self.f}, state={self.state})'

    def __lt__(self, other):
        """Defines less than operator for node objects with respect to
            f-value."""
        return self.f < other.f

    def __le__(self, other):
        """Defines less than or equal to operator for node objects with
            respect to f-value."""
        return self.f <= other.f

    def __gt__(self, other):
        """Defines greater than operator for node objects with respect
            to f-value."""
        return self.f > other.f

    def __ge__(self, other):
        """Defines greater than or equal to operator for node objects
            with respect to f-value."""
        return self.f >= other.f

    def __eq__(self, other):
        """Defines equality of nodes to be based on underlying state."""
        return self.state == other.state
