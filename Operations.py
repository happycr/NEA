import Types
from Errors import TranslationError
from Unionise import Unionise

"""
Operations class: provides function do compute the type of basic arithmetic and logical expressions.
Note that all the methods have the @Unionize decorator, which is a custom built decorator defined in the Unionize file.
This decorator allows the methods to deal with union types.
"""


class Operations:
    """
    Add method. Called by the type checker when two objects are added together.
    We have used pattern matching, available in the newest python version, to implement it.
    """

    @staticmethod
    @Unionise
    def add(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Int
            case (Types.Int, Types.Real):
                return Types.Real
            case (Types.Real, Types.Int):
                return Types.Real
            case (Types.Real, Types.Real):
                return Types.Real
            case (Types.String, Types.String):
                return Types.String
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot add objects of type {x.getName()} and {y.getName()}")

    """
    Multiply method. Called by the type checker when two objects are multiplied together.
    """

    @staticmethod
    @Unionise
    def multiply(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Int
            case (Types.Int, Types.Real):
                return Types.Real
            case (Types.Real, Types.Int):
                return Types.Real
            case (Types.Real, Types.Real):
                return Types.Real
            case (Types.String, Types.Int):
                return Types.String
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot multiply objects of type {x.getName()} and {y.getName()}")

    """
    Mod method. Called by the type checker when two objects are MODded together.
    """

    @staticmethod
    @Unionise
    def mod(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Int
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot mod objects of type {x.getName()} and {y.getName()}")

    """
    Div method. Called by the type checker when two objects are DIV together.
    """

    @staticmethod
    @Unionise
    def div(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Int
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot div objects of type {x.getName()} and {y.getName()}")

    """
    Subtract method. Called by the type checker when two objects are subtracted together.
    """

    @staticmethod
    @Unionise
    def subtract(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Int
            case (Types.Int, Types.Real):
                return Types.Real
            case (Types.Real, Types.Int):
                return Types.Real
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot subtract objects of type {x.getName()} and {y.getName()}")

    """
    Divide method. Called by the type checker when two objects are divided together.
    """

    @staticmethod
    @Unionise
    def divide(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Real
            case (Types.Int, Types.Real):
                return Types.Real
            case (Types.Real, Types.Int):
                return Types.Real
            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot divide objects of type {x.getName()} and {y.getName()}")

    """
    Compare method. This method handles any comparison operators: >, <, ≤, ≥, =, ≠
    Called by the type checker when two objects are compared.
    """
    @staticmethod
    @Unionise
    def compare(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Int, Types.Int):
                return Types.Bool
            case (Types.String, Types.String):
                return Types.Bool
            case (Types.Real, Types.Int):
                return Types.Bool
            case (Types.Int, Types.Real):
                return Types.Bool
            case (Types.Real, Types.Real):
                return Types.Bool

            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(f"Cannot compare objects of type {x.getName()} and {y.getName()}")

    """
    This method handles any logical operators: AND, OR.
    Called by the type checker for AND, OR operators
    """
    @staticmethod
    @Unionise
    def bool_operation(x: Types.Type, y: Types.Type) -> Types.Type:
        match (x, y):
            case (Types.Bool, Types.Bool):
                return Types.Bool

            # In the default case raise an error, signaling an invalid expression.
            case (_, _):
                raise TranslationError(
                    f"Cannot use a logical boolean operation on objects of type {x.getName()} and {y.getName()}")

    """
    NOT method. Called by the type checker for NOT operator.
    Since NOT is a unary operator, this method only accepts one parameter, contrary to the methods above.
    The Unionize decorator still works as it was implemented with a variable number of arguments.
    """

    @staticmethod
    @Unionise
    def Not(x: Types.Type) -> Types.Type:
        match x:
            case (Types.Bool):
                return Types.Bool
            # In the default case raise an error, signaling an invalid expression.
            case (_):
                raise TranslationError(f"Cannot use not on object of type {x.getName()}")

    """
    minus method. Called by the type checker for the unary minus operator.
    This method only accepts one parameter, similar to the NOT method.
    """
    @staticmethod
    @Unionise
    def minus(x: Types.Type) -> Types.Type:
        match x:
            case (Types.Real):
                return Types.Real
            case (Types.Int):
                return Types.Int
            # In the default case raise an error, signaling an invalid expression.
            case (_):
                raise TranslationError(f"Cannot apply minus on object of type {x.getName()}")
