from collections import namedtuple

Problem = namedtuple('Problem', 'initial goal epsilon statics', defaults=(1, []))

# Problem.__defaults__ = (1, [])