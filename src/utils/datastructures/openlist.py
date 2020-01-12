"""Open-list data structure for use in search.

Typical usage:

open_list = OpenList()
open_list.append(node)
for node in open_list:
    print(node)
"""

__all__ = ['OpenList']

from math import inf
import heapq

from src.utils.datastructures.node import Node


class OpenList:
    """Open-list data structure.

    Attributes:
        openlist: A min-heap intended to contain state objects.
        g_tracker: A min-heap storing the different g-values in the
            open-list
    """

    def __init__(self):
        """Initializes open-list with an empty list."""
        self.openlist = []
        self.g_tracker = []

    def append(self, node):
        """Adds a node to the openlist. Updates the g_tracker
        attribute to account for the new node's g-value.

        Args:
            node: Expected to be of type Node.
        """
        heapq.heappush(self.openlist, node)
        heapq.heappush(self.g_tracker, node.g)

    def pop(self):
        """Removes and returns the highest-priority element in
        open-list.

        Returns:
            Object of type Node, with highest priority in open-list.
        """
        out = heapq.heappop(self.openlist)
        return out

    def peek(self):
        """Returns highest-priority element in open-list without
        removing it.

        Returns:
            Object of type Node, with highest priority in open-list.
        """
        return self.openlist[0]

    def get_g(self, state):
        """Returns the g-value of a node in the open-list, as specified
        by the node's state. If node is not found, default value of
        infinity is returned.

        Args:
            state: State object of node requested.

        Returns:
            g-value of node associated with state, in the open list.
        """
        for other in self.openlist:
            if other.state == state:
                return other.g
        return inf

    def get(self, state):
        """Returns from the open-list the node associated with
        specified state.

        Args:
            state: State object of node requested.

        Returns:
            Node object from open-list with state attribute
                equal to state input.

        Raises:
            Exception if no node with provided state exists in open-list.
        """
        for other in self.openlist:
            print(other.state, state)
            if other.state == state:
                return other
        raise Exception("Node not found.")

    def replace(self, obj, other):
        """Replaces a node in the open-list with a new node.

        Args:
            obj: Object of type Node or State.
            other: Node object, to replace obj.

        Raises:
            Exception if no node with specified state exists in
                open-list.
        """
        state = self._node_to_state(obj)
        for i, x in enumerate(self.openlist):
            if x.state == state:
                self.g_tracker.pop(self.g_tracker.index(x.g))
                heapq.heapify(self.g_tracker)
                self.openlist[i] = other
                break
        else:
            raise Exception("Node not found.")
        heapq.heappush(self.g_tracker, other.g)


    def remove(self, obj):
        """Removes a specified node from the open-list.

        Args:
            obj: Object of type Node or State.

        Raises:
            Exception if no node with specified state exists in
                open-list.
        """

        state = self._node_to_state(obj)
        for i in range(len(self.openlist)):
            if self.openlist[i].state == state:
                self.g_tracker.pop(self.g_tracker.index(self.openlist[i].g))
                heapq.heapify(self.g_tracker)
                break
        else:
            raise Exception("Node not found.")

        self.openlist.pop(i)
        heapq.heapify(self.openlist)

    def min_g(self):
        """Returns the least g-value among nodes in the open list.

        Returns:
            An integer value.
        """
        out = heapq.heappop(self.g_tracker)
        heapq.heappush(self.g_tracker, out)
        return out

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

    def __repr__(self):
        """Simple representation method for OpenList"""
        return str(self.openlist)

    def __str__(self):
        """String representation method for OpenList. Provides info
        on size, minimum and maximum f/g values of nodes.
        """
        out = f"""Size: {len(self.openlist)}
g values: (min: {self.min_g}, max: {self.max_g})
f values: (min: {self.min_f}, max: {self.max_f})"""
        return out

    def __len__(self):
        """Simple len method for OpenList"""
        return len(self.openlist)

    def __getitem__(self, item):
        """Simple getitem method for OpenList, allows for iteration
        and indexing.
        """
        return self.openlist[item]

    def __contains__(self, obj):
        """Simple contains method for OpenList. Accepts either State or
        Node objects.
        """
        state = self._node_to_state(obj)
        return any(other.state == state for other in self.openlist)
