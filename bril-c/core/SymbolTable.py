from abc import ABC
from Types import Type, CharType, VoidType

class SymbolInfo(ABC):
    """Abstract base class for all symbol information."""
    def __init__(self, name: str, scope: str):
        self.name = name
        self.scope = scope

    def __repr__(self):
        return f"SymbolInfo(name={self.name}, scope={self.scope})"

class VarInfo(SymbolInfo):
    def __init__(self, name: str, var_type: Type, scope: str, initialized=False, is_const=False):
        super().__init__(name, scope)
        self.var_type = var_type
        self.initialized = initialized
        self.is_const = is_const

    def __repr__(self):
        return (f"VarInfo(name={self.name}, type={self.var_type.type_name()}, "
                f"scope={self.scope}, initialized={self.initialized}, is_const={self.is_const})")


class FunInfo(SymbolInfo):
    def __init__(self, name: str, param_types: list[Type], return_type: Type, scope: str, param_names=None):
        super().__init__(name, scope)
        self.param_types = param_types
        self.return_type = return_type
        self.param_names = param_names if param_names else []

    def __repr__(self):
        param_str = ", ".join([ptype.type_name() for ptype in self.param_types])
        return (f"FunInfo(name={self.name}, params=[{param_str}], "
                f"return={self.return_type.type_name()}, scope={self.scope})")


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes

    def enter_scope(self):
        """Enter a new scope."""
        self.scopes.append({})

    def exit_scope(self):
        """Exit the current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise RuntimeError("Cannot exit the global scope")

    def declare_symbol(self, name: str, symbol_entry: SymbolInfo):
        """Declare a new symbol (variable or function) in the current scope."""
        if name in self.scopes[-1]:
            raise RuntimeError(f"Symbol '{name}' already declared in the current scope")
        self.scopes[-1][name] = symbol_entry

    def lookup_symbol(self, name: str) -> SymbolInfo:
        """Look up a symbol (variable or function) by name."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Symbol '{name}' not declared")

    def __repr__(self):
        return f"SymbolTable(scopes={self.scopes})"

class UnifiedSymbolTable:
    def __init__(self):
        self.var_table = SymbolTable()  # For variables
        self.func_table = SymbolTable()  # For functions

        # Preload built-in functions
        self._initialize_builtin_functions()

    def _initialize_builtin_functions(self):
        """
        Preload built-in functions such as printf.
        """
        printf_info = FunInfo(
            name="printf",
            param_types=[VoidType()],  # TODO: variadic arg
            return_type=VoidType(),
            scope="global",
            param_names=["format"]
        )
        self.declare_function("printf", printf_info)

    def enter_scope(self):
        """Enter a new scope for both variable and function tables."""
        self.var_table.enter_scope()
        self.func_table.enter_scope()

    def exit_scope(self):
        """Exit the current scope for both variable and function tables."""
        self.var_table.exit_scope()
        self.func_table.exit_scope()

    def declare_variable(self, name: str, var_entry: VarInfo):
        """Declare a variable in the variable table."""
        self.var_table.declare_symbol(name, var_entry)

    def declare_function(self, name: str, func_entry: FunInfo):
        """Declare a function in the function table."""
        self.func_table.declare_symbol(name, func_entry)

    def lookup_variable(self, name: str) -> VarInfo:
        """Look up a variable in the variable table."""
        return self.var_table.lookup_symbol(name)

    def lookup_function(self, name: str) -> FunInfo:
        """Look up a function in the function table."""
        return self.func_table.lookup_symbol(name)
