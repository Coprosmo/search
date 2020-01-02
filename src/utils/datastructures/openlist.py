from _collections import namedtuple

__dict__.__all__ = ['OpenList']


class OpenList:
    """Open list object with optional bidirectional capabilities."""
    def __init__(self,
                 sortattr: 'Optional argument, defines the priority attribute to use in queue' = None,
                 bidir: 'Defines bidirectional nature of open list' = False):

        if bidir:
            Open = namedtuple('Open', 'fw bw')
            self.open = Open(list, list)
        else:
            self.open = list

        self.sortattr = sortattr
