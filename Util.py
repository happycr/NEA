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

def remove_duplicates(type_list):
    newlist = []
    for _type in type_list:
        _type = _type.getUnderlyingType()
        for flat_type in _type:
            if flat_type not in newlist:
                newlist.append(flat_type)
    return newlist


    return newlist
