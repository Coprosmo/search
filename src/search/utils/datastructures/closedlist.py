"""Closed-list data structure for use in search.

    Typical usage:

    closed_list = ClosedList()
    closed_list.append(node)
    for node in closed_list:
        print(node)
"""

from .node import Node

__all__ = ['ClosedList']


class ClosedList:
    """Closed-list data structure.

    Attributes:
        closedlist: A set intended to contain state objects.
    """

    def __init__(self):
        """Initializes ClosedList with an empty set."""
        self.closedlist = set()

    def append(self, node):
        """Adds a node's state to the closed-list.

        Args:
            node: A node object.
        """
        self.closedlist.add(node.state)

    def remove(self, obj):
        """Removes the state associated with a specified object from the closed-list.

        Args:
            obj: An object of type either Node or State.
        """
        state = self._node_to_state(obj)
        self.closedlist.remove(state)

    def _node_to_state(self, obj):
        """Checks if an object is a node or a state, and returns the associated state.

        Args:
            obj: An object of type either Node or State.

        Returns:
            An object of type state, associated with obj.
        """
        if isinstance(obj, Node):
            return obj.state
        else:
            return obj

    def __len__(self):
        """Returns the length of closedlist attribute"""
        return len(self.closedlist)

    def __contains__(self, obj):
        """Simple __contains__ method for closedlist attribute.
        Returns True if the state associated with obj is in closedlist,
        otherwise returns False.

        Args:
            obj: An object of type either Node or State.

        Returns:
            A boolean value.
        """
        state = self._node_to_state(obj)
        return state in self.closedlist

    def __iter__(self):
        """Simple iterator method for ClosedList. Returns an iterator
        for the set closedlist.

        Returns:
            An iterator for closedlist attribute.
        """
        return iter(self.closedlist)

