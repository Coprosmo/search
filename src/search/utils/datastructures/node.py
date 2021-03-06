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
        self.expanded_once = False
        self.expanded_nonce = False

    def expand(self, problem, partial_expansion=False, gen_limit=None):
        """Expands node, to give all directly reachable children.

        Returns:
            A generator object for the successors of node's state.
        """
        if self.G is None:
            print('Breaking!')
        if partial_expansion == "g":
            successors = self.state.successors(problem)
            for i in range(self.n_expanded, len(successors)):
                if self.is_fully_expanded():
                    break

                state, cost = successors[i]
                temp_g = self.g + cost

                # TODO: Fix this to check if <= gen_limit_1 OR (<= gen_limit_2 AND collides with opposite side)
                #if self.do_generate(state, cost, gen_limit_1, gen_limit_2, opp_open):
                if temp_g <= gen_limit:
                    if temp_g == self.G:
                        self.n_expanded += 1
                        if i + 1 == self.state.n_successors:
                            self.G = None
                        yield state, temp_g
                    elif temp_g > self.G:
                        self.G = temp_g
                        break
                else:
                    self.G = temp_g
                    break

        else:
            for state, cost in self.state.successors(problem):
                self.n_expanded += 1
                yield state, self.g + cost

    def path(self, reverse=False):
        """Gives the path from the initial state to node's state.
        Ordinarily reverses path at end so correct order, so if
        argument reverse=True is specified, this is not done.

        Args:
            reverse: An optional argument. If True, returns path in
                reversed order.

        Returns:
            Tuple object containing the ordered path from initial
                state to current state. Contains node objects.
        """
        node, path_back = self, []
        while node:
            path_back.append((node.g, node.state.state))
            node = node.parent
        if reverse:
            out = tuple(path_back)
        else:
            out = tuple(reversed(path_back))
        return out

    def is_fully_expanded(self):
        """Returns a boolean value describing whether node has been
        fully expanded. Intended for use in deferred expansion search.

        Returns:
            A boolean value, True if node has been expanded, otherwise
                False.
        """
        return self.G is None or self.n_expanded == self.state.n_successors

    def do_generate(self, child_state, child_g, gen_limit_1, gen_limit_2, opp_open):
        return any((child_g <= gen_limit_1,
                   child_g <= gen_limit_2 and child_state in opp_open))

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
