from abc import ABC, abstractmethod, ABCMeta

# Base Type class
class Type(ABC):
    """Abstract base class for all types."""

    def is_same_type(self, other: 'Type') -> bool:
        """Check if two types are the same based on their instance."""
        return self is other

    @abstractmethod
    def type_name(self) -> str:
        """Return the name of the type."""
        raise NotImplementedError
    
    @staticmethod
    def from_string(type_name: str) -> 'Type':
        """Factory method to create a Type instance from a string."""
        type_map = {
            "int": IntType(),
            "float": FloatType(),
            "bool": BoolType(),
            "char": CharType(),
            "void": VoidType(),
            "string": StringType(),
        }
        if type_name in type_map:
            return type_map[type_name]
        else:
            raise ValueError(f"Unknown type name: {type_name}")



# Singleton Metaclass for Types
class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Concrete Types
class IntType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "int"


class FloatType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "float"


class BoolType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "bool"


class CharType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "char"


class VoidType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "void"
    

class StringType(Type, metaclass=SingletonMeta):
    def type_name(self) -> str:
        return "string"