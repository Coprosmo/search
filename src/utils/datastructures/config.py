from collections import namedtuple

__all__ = ['Config']

Config = namedtuple('Config', """seed
                                    domain
                                    algs
                                    partial_expansion
                                    param""")

Config.__defaults__ = (None,)