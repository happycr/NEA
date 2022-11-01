import Types
from Errors import CustomError
from Util import Unionize


@Unionize
def add(x: Types.Type, y: Types.Type) -> Types.Type:  # type: ignore
    """Returns the resultant types from adding two types together."""
    match (x, y):
        case (Types.Int, Types.Int): return Types.Int
        case (Types.Int, Types.Real): return Types.Real
        case (Types.Real, Types.Int): return Types.Real
        case (Types.Real, Types.Real): return Types.Real
        case (Types.String, Types.String): return Types.String
        case (_, _): raise CustomError(f"Cannot add objects of type {x.name} and {y.name}")


@Unionize
def multiply(x: Types.Type, y: Types.Type) -> Types.Type:  # type: ignore
    match (x, y):
        case (Types.Int, Types.Int): return Types.Int
        case (Types.Int, Types.Real): return Types.Real
        case (Types.Real, Types.Int): return Types.Real
        case (Types.String, Types.Int): return Types.String
        case (_, _): raise CustomError(f"Cannot multiply objects of type {x.name} and {y.name}")


@Unionize
def mod(x: Types.Type, y: Types.Type) -> Types.Type:
    match (x,y):
        case (Types.Int, Types.Int): return Types.Int
        case(_, _): raise CustomError(f"Cannot mod objects of type {x.name} and {y.name}")


@Unionize
def div(x: Types.Type, y: Types.Type) -> Types.Type:
    match(x,y):
        case(Types.Int, Types.Int): return Types.Int
        case(_, _): raise CustomError(f"Cannot div objects of type {x.name} and {y.name}")


@Unionize
def subtract(x: Types.Type, y: Types.Type) -> Types.Type:
    match(x,y):
        case(Types.Int, Types.Int): return Types.Int
        case(Types.Int, Types.Real): return Types.Real
        case(Types.Real, Types.Int): return Types.Real


@Unionize
def divide(x: Types.Type, y: Types.Type) -> Types.Type:
    match(x,y):
        case(Types.Int, Types.Int): return Types.Real
        case(Types.Int, Types.Real):return Types.Real
        case(Types.Real, Types.Int): return Types.Real
        case(_, _): raise CustomError(f"Cannot divide objects of type {x.name} and {y.name}")

@Unionize
def compare(x: Types.Type, y: Types.Type) -> Types.Type:
    match (x,y):
        case(Types.Int, Types.Int): return Types.Bool
        case (Types.String, Types.String): return Types.Bool
        case (Types.Real, Types.Int): return Types.Bool
        case (Types.Int, Types.Real): return Types.Bool
        case (Types.Real, Types.Real): return Types.Bool
        case(_, _): raise CustomError(f"Cannot compare objects of type {x.name} and {y.name}")

@Unionize
def bool_operation(x: Types.Type, y: Types.Type) -> Types.Type:
    match (x,y):
        case(Types.Bool, Types.Bool): return Types.Bool
        case(_, _): raise CustomError(f"Cannot use a logical boolean operation on objects of type {x.name} and {y.name}")

@Unionize
def Not(x: Types.Type) -> Types.Type:
    match x:
        case(Types.Bool): return Types.Bool
        case(_): raise CustomError(f"Cannot use not on object of type {x.name}")

@Unionize
def minus(x: Types.Type) -> Types.Type:
    match x:
        case (Types.Real): return Types.Real
        case (Types.Int): return Types.Int
        case(_): raise CustomError(f"Cannot apply minus on object of type {x.name}")












