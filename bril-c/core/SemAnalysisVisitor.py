from CVisitor import CVisitor
from CParser import CParser
from SymbolTable import UnifiedSymbolTable, VarInfo, FunInfo
from Types import IntType, FloatType, BoolType, CharType, StringType, Type


class SemAnalysisVisitor(CVisitor):
    def __init__(self, debug_mode=False):
        self.symbol_table = UnifiedSymbolTable()
        self.debug_mode = debug_mode

    def debug(self, content):
        if self.debug_mode:
            print(content)

    def visitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        """
        Handles function definitions and manages function scope.
        """
        func_name = ctx.declarator().getText().split('(')[0]  # Remove parentheses for function name
        param_types = []  # TODO: Extract parameter types from the context
        return_type = self.determine_type(ctx.declarationSpecifiers().getText())

        func_info = FunInfo(func_name, param_types, return_type, "global")
        try:
            self.symbol_table.declare_function(func_name, func_info)
            self.debug(f"Declared function: {func_name}, return type: {return_type.type_name()}")
        except RuntimeError as e:
            raise RuntimeError(f"[visitFunctionDefinition] {e}")

        self.debug(f"Entering function scope: {func_name}")
        self.symbol_table.enter_scope()  # Enter function scope
        self.visit(ctx.compoundStatement())  # Visit function body
        self.symbol_table.exit_scope()  # Exit function scope
        self.debug(f"Exiting function scope: {func_name}")

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles variable declarations.
        """
        var_name = ctx.initDeclaratorList().initDeclarator(0).declarator().getText()
        var_type = self.determine_type(ctx.declarationSpecifiers().getText())

        try:
            var_info = VarInfo(var_name, var_type, "local" if len(self.symbol_table.var_table.scopes) > 1 else "global")
            self.symbol_table.declare_variable(var_name, var_info)
            self.debug(f"Declared variable: {var_name}, type: {var_type.type_name()}")
        except RuntimeError as e:
            raise RuntimeError(f"[visitDeclaration] {e}")

    def visitSelectionStatement(self, ctx: CParser.SelectionStatementContext):
        if ctx.If():
            self.visit(ctx.expression())
            # check expression type?
            self.visit(ctx.statement(0))
            if ctx.Else():
                self.visit(ctx.statement(1))

    def visitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        """
        Handles assignment expressions and performs type checks.
        """
        if ctx.getChildCount() == 3 and ctx.assignmentOperator():
            var_name = ctx.getChild(0).getText()
            expr_type = self.visit(ctx.getChild(2))  # Visit right-hand side expression

            try:
                var_info = self.symbol_table.lookup_variable(var_name)
                if not var_info.var_type.is_same_type(expr_type):
                    raise TypeError(f"Type mismatch: {var_name} is {var_info.var_type.type_name()}, but got {expr_type.type_name()}")
                var_info.initialized = True
                self.debug(f"Assigned value to variable: {var_name}")
            except RuntimeError as e:
                raise RuntimeError(f"[visitAssignmentExpression] {e}")
        else:
            return self.visit(ctx.getChild(0))  # Handle other assignment expressions

    def visitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        """
        Handles addition and subtraction with type checks.
        """
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left_type = self.visit(ctx.getChild(0))
        right_type = self.visit(ctx.getChild(2))

        if not left_type.is_same_type(right_type):
            raise TypeError(f"Type mismatch in additive expression: {left_type.type_name()} vs {right_type.type_name()}")
        return left_type

    def visitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        """
        Handles primary expressions (identifiers and constants).
        """
        if ctx.Identifier():
            var_name = ctx.Identifier().getText()
            try:
                var_info = self.symbol_table.lookup_variable(var_name)
                return var_info.var_type
            except RuntimeError:
                pass

            try:
                func_info = self.symbol_table.lookup_function(var_name)
                return func_info.return_type
            except RuntimeError as e:
                raise RuntimeError(f"[visitPrimaryExpression] {e}")
        elif ctx.Constant():
            return IntType()  # TODO: Assume constants are integers
        elif ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.StringLiteral():
            return StringType()
        else:
            raise NotImplementedError("Unsupported primary expression")

    def determine_type(self, type_str: str) -> Type:
        """
        Maps string representation of types to Type objects.
        """
        if type_str == "int":
            return IntType()
        elif type_str == "float":
            return FloatType()
        elif type_str == "bool":
            return BoolType()
        elif type_str == "char":
            return CharType()
        else:
            raise TypeError(f"Unknown type: {type_str}")
