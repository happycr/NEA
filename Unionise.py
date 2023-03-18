import itertools

import Types

"""
Unionize function which defines a custom built operator. Helps deal operation with union types. 
When applying an operation to union types, we must find out every possible return type and take the union of those.
For example:
(Integer | Real | String) * Integer = ( Integer * Integer) | ( Real * Integer) | ( String * Integer)
= Integer | Real | String

The Unionize function takes as an input a function, which takes non union types as arguments.
The Unionize function then returns a new function, which is able to take union types as arguments.
This is done by using the cartesian product algorithm.
"""


def Unionise(func):
    def inner(*args):
        # Get cartesian product of list of types.
        list_of_types = [x for x in itertools.product(*args)]
        # If there is only one possible type combination, return the operation applied to that combination.
        if len(list_of_types) == 1:
            return func(*list_of_types[0])
        # If there are multiple  type combinations, return the union of the operation applied to all the combinations.
        else:
            return Types.UnionType([func(*x) for x in list_of_types])

    return inner
