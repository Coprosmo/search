
__all__ = ['ClosedList']

class ClosedList:
    def __init__(self):
        self.closedlist = set()

    def append(self, node):
        self.closedlist.add(node)

    def __len__(self):
        return len(self.closedlist)

    def __contains__(self, node):
        state = node.state
        return state in self.closedlist

