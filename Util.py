import itertools

import Types


def Unionize(func):
    def inner(*args):
        list_of_types = [x for x in CartesianProduct(*args)]
        if len(list_of_types) == 1:
            return func(*list_of_types[0])
        else:
            return Types.UnionType([func(*x) for x in list_of_types])
    return inner


def CartesianProduct(*args):
    for i in itertools.product(*args):
        yield i


def remove_duplicates(L):
    newlist = [ii for n, ii in enumerate(L) if ii not in L[:n]]
    return newlist
