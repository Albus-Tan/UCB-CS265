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