from CVisitor import CVisitor
from CParser import CParser
from SymbolTable import UnifiedSymbolTable, VarInfo, FunInfo
from Types import IntType, FloatType, BoolType, CharType, StringType, VoidType, Type


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

        # Extract function parameters
        param_list = []
        if ctx.declarator().directDeclarator().parameterTypeList():
            param_decls = ctx.declarator().directDeclarator().parameterTypeList().parameterList()
            for param_decl in param_decls.parameterDeclaration():
                param_name = param_decl.declarator().getText()
                param_type_str = param_decl.declarationSpecifiers().getText()
                param_list.append({"name": param_name, "type": Type.from_string(param_type_str)})

        return_type = Type.from_string(ctx.declarationSpecifiers().getText())

        func_info = FunInfo(func_name, [param["type"] for param in param_list], return_type, "global")
        try:
            self.symbol_table.declare_function(func_name, func_info)
            self.debug(f"Declared function: {func_name}, return type: {return_type.type_name()}")
        except RuntimeError as e:
            raise RuntimeError(f"[visitFunctionDefinition] {e}")

        self.debug(f"Entering function scope: {func_name}")
        self.symbol_table.enter_scope()  # Enter function scope

        # Init function paramater in symbol_table
        for param_info in param_list:
            self.symbol_table.declare_variable(param_info["name"], VarInfo(param_info["name"], param_info["type"], "local"))

        self.visit(ctx.compoundStatement())  # Visit function body
        self.symbol_table.exit_scope()  # Exit function scope
        self.debug(f"Exiting function scope: {func_name}")

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles variable declarations.
        """
        if not ctx.initDeclaratorList():
            return
        var_name = ctx.initDeclaratorList().initDeclarator(0).declarator().getText()
        var_type = Type.from_string(ctx.declarationSpecifiers().getText())

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
        else:
            raise NotImplementedError("Unsupported selection statement")

    def visitIterationStatement(self, ctx: CParser.IterationStatementContext):
        if ctx.For():
            children = list(ctx.forCondition().getChildren())
            semicolon_indices = [i for i, child in enumerate(children) if child.getText() == ';']
            if ctx.forCondition().forDeclaration():
                self.visit(ctx.forCondition().forDeclaration())
            elif ctx.forCondition().expression():
                self.visit(ctx.forCondition().expression())

            for_expressions = ctx.forCondition().forExpression()
            if len(for_expressions) == 1:
                expr_index = children.index(for_expressions[0])
                if expr_index < semicolon_indices[1]:
                    # Condition
                    self.visit(for_expressions[0])
                else:
                    # Increment
                    self.visit(for_expressions[0])
            else:
                self.visit(for_expressions[0])
                self.visit(for_expressions[1])

            self.visit(ctx.statement())
        else:
            raise NotImplementedError("Unsupported iteration statement")

    def visitForDeclaration(self, ctx):
        return self.visitDeclaration(ctx)

    def visitForExpression(self, ctx: CParser.ForExpressionContext):
        for expr in ctx.assignmentExpression():
            self.visit(expr)

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
            if var_name in ["true", "false"]:
                return BoolType()
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
