from CParser import CParser
from CVisitor import CVisitor
from SymbolTable import SymbolTable, FunInfo
from Types import Type, VoidType


class CToBrilVisitor(CVisitor):
    def __init__(self, debug_mode):
        self.bril_program = {"functions": []}
        self.current_function = None
        self.temp_var_counter = 0
        self.if_counter = 0
        self.for_counter = 0
        self.debug_mode = debug_mode

        # Global function symbol table
        self.func_table = SymbolTable()

    def debug(self, content):
        if self.debug_mode:
            print(content)

    def declare_function(self, name: str, func_entry: FunInfo):
        """Declare a function in the function table."""
        self.func_table.declare_symbol(name, func_entry)

    def lookup_function(self, name: str) -> FunInfo:
        """Look up a function in the function table."""
        return self.func_table.lookup_symbol(name)

    def generate_temp_var(self):
        temp_var = f"temp_{self.temp_var_counter}"
        self.temp_var_counter += 1
        return temp_var

    # Primary expressions: variables, constants, or parenthesized expressions
    def visitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        if ctx.Identifier():
            var_name = ctx.Identifier().getText()
            if var_name in ["true", "false"]:
                temp_var = self.generate_temp_var()
                self.current_function["instrs"].append({
                    "op": "const",
                    "dest": temp_var,
                    "type": "bool",
                    "value": True if var_name == "true" else False
                })
                return temp_var
            else:
                return var_name
        elif ctx.Constant():
            # Int, Float and Char
            temp_var = self.generate_temp_var()
            value = ctx.Constant().getText()

            if value.isdigit():
                const_type = "int"
                const_value = int(value)
            elif value.replace('.', '', 1).isdigit() and '.' in value:
                const_type = "float"
                const_value = float(value)
            elif len(value) == 3 and value.startswith("'") and value.endswith("'"):
                const_type = "char"
                const_value = value[1]
            else:
                raise NotImplementedError(f"Unsupported constant: {value}")

            # Append the instruction for the constant
            self.current_function["instrs"].append({
                "op": "const",
                "dest": temp_var,
                "type": const_type,
                "value": const_value
            })
            return temp_var
        elif ctx.expression():
            return self.visit(ctx.expression())
        elif ctx.StringLiteral():
            string_value = ''.join([literal.getText().strip('"') for literal in ctx.StringLiteral()])
            return string_value
        else:
            raise NotImplementedError

    def visitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        func_name = ctx.declarator().directDeclarator().directDeclarator().getText()

        # Extract function arguments
        param_list = []
        if ctx.declarator().directDeclarator().parameterTypeList():
            param_decls = ctx.declarator().directDeclarator().parameterTypeList().parameterList()
            for param_decl in param_decls.parameterDeclaration():
                param_name = param_decl.declarator().getText()
                param_type_str = param_decl.declarationSpecifiers().getText()
                param_list.append({"name": param_name, "type": param_type_str})

        self.debug(f"[visitFunctionDefinition] Function {func_name}() extracted arguments: {param_list}")

        # Construct function object
        self.current_function = {
            "name": func_name,
            "args": param_list,
            "instrs": []
        }

        # Add return type if not main and return type is not void
        return_type = ctx.declarationSpecifiers().getText()
        if func_name != "main" and return_type != "void":
            self.current_function["type"] = return_type

        # Register the function in symbol table
        func_info = FunInfo(
            name=func_name,
            param_types=[Type.from_string(param["type"]) for param in param_list],
            return_type=Type.from_string(return_type),
            scope="global"
        )
        self.declare_function(func_name, func_info)

        # Visit the function body
        self.visit(ctx.compoundStatement())
        self.bril_program["functions"].append(self.current_function)

    def visitDeclaration(self, ctx: CParser.DeclarationContext):
        # TODO: support initDeclaratorList
        var_name = ctx.initDeclaratorList().initDeclarator(0).declarator().getText()
        initializer = ctx.initDeclaratorList().initDeclarator(0).initializer()
        var_type = ctx.declarationSpecifiers().getText()

        expr_result = self.visit(initializer.assignmentExpression())

        self.current_function["instrs"].append({
            "op": "id",
            "dest": var_name,
            "type": var_type,
            "args": [expr_result]
        })

    def visitSelectionStatement(self, ctx):
        if ctx.If():
            expr_result = self.visit(ctx.expression())
            if_counter = self.if_counter
            self.if_counter += 1
            if ctx.Else():
                self.current_function["instrs"].append({
                    "op": "br",
                    "args": [expr_result],
                    "labels": [f"if_then_{if_counter}", f"if_else_{if_counter}"]
                })
            else:
                self.current_function["instrs"].append({
                    "op": "br",
                    "args": [expr_result],
                    "labels": [f"if_then_{if_counter}", f"if_exit_{if_counter}"]
                })
            self.current_function["instrs"].append({
                "label": f"if_then_{if_counter}"
            })
            self.visit(ctx.statement(0))
            if ctx.Else():
                self.current_function["instrs"].append({
                    "op": "jmp",
                    "labels": [f"if_exit_{if_counter}"]
                })
                self.current_function["instrs"].append({
                    "label": f"if_else_{if_counter}"
                })
                self.visit(ctx.statement(1))
            self.current_function["instrs"].append({
                "label": f"if_exit_{if_counter}"
            })
        else:
            raise NotImplementedError

    def visitIterationStatement(self, ctx: CParser.IterationStatementContext):
        if ctx.For():
            children = list(ctx.forCondition().getChildren())
            semicolon_indices = [i for i, child in enumerate(children) if child.getText() == ';']
            if ctx.forCondition().forDeclaration():
                self.visit(ctx.forCondition().forDeclaration())
            elif ctx.forCondition().expression():
                self.visit(ctx.forCondition().expression())

            for_condition = None
            for_increment = None
            for_expressions = ctx.forCondition().forExpression()
            if len(for_expressions) == 1:
                expr_index = children.index(for_expressions[0])
                if expr_index < semicolon_indices[1]:
                    for_condition = for_expressions[0]
                else:
                    for_increment = for_expressions[0]
            else:
                for_condition = for_expressions[0]
                for_increment = for_expressions[1]

            for_counter = self.for_counter
            self.for_counter += 1
            self.current_function["instrs"].append({
                "label": f"for_cond_{for_counter}"
            })
            if for_condition:
                expr_result = self.visit(for_condition)
                self.current_function["instrs"].append({
                    "op": "br",
                    "args": [expr_result],
                    "labels": [f"for_body_{for_counter}", f"for_exit_{for_counter}"]
                })
            self.current_function["instrs"].append({
                "label": f"for_body_{for_counter}"
            })
            self.visit(ctx.statement())
            if for_increment:
                self.visit(for_increment)
            self.current_function["instrs"].append({
                "op": "jmp",
                "labels": [f"for_cond_{for_counter}"]
            })
            self.current_function["instrs"].append({
                "label": f"for_exit_{for_counter}"
            })
        else:
            raise NotImplementedError("Unsupported iteration statement")

    def visitForDeclaration(self, ctx):
        return self.visitDeclaration(ctx)

    def visitForExpression(self, ctx: CParser.ForExpressionContext):
        ret = None
        for expr in ctx.assignmentExpression():
            ret = self.visit(expr)
        return ret

    def visitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        if ctx.getChildCount() == 3 and ctx.assignmentOperator():
            var_name = ctx.getChild(0).getText()
            operator = ctx.getChild(1).getText()
            right_expr_result = self.visit(ctx.getChild(2))

            if operator == "=":
                # TODO: support more types, currently none types other than int can be assigned
                # We need more advanced type system
                self.current_function["instrs"].append({
                    "op": "id",
                    "dest": var_name,
                    "type": "int",
                    "args": [right_expr_result]
                })
            else:
                base_op = {
                    "+=": "add",
                    "-=": "sub",
                    "*=": "mul",
                    "/=": "div",
                    "&=": "and",
                    "|=": "or"
                }.get(operator)

                if base_op:
                    # TODO: support more types
                    temp_var = self.generate_temp_var()
                    self.current_function["instrs"].append({
                        "op": base_op,
                        "dest": temp_var,
                        "args": [var_name, right_expr_result],
                        "type": "int"
                    })
                    self.current_function["instrs"].append({
                        "op": "id",
                        "dest": var_name,
                        "type": "int",
                        "args": [temp_var]
                    })
                else:
                    raise NotImplementedError
        else:
            # Deal with other types of assignmentExpression (e.g. conditionalExpression)
            return self.visit(ctx.getChild(0))

    def visitPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        base_expr = self.visit(ctx.getChild(0))

        if ctx.getChildCount() > 1:
            for i in range(1, ctx.getChildCount(), 2):
                # Function Call
                if ctx.getChild(i).getText() == '(':
                    func_name = base_expr
                    args = []
                    if ctx.getChild(i + 1).getText() != ')':
                        arg_list = ctx.getChild(i + 1)
                        for arg in arg_list.getChildren():
                            if isinstance(arg, CParser.AssignmentExpressionContext):
                                args.append(self.visit(arg))

                    if func_name == "printf":
                        for arg in args[1:]:
                            self.current_function["instrs"].append({
                                "op": "print",
                                "args": [arg]
                            })
                    else:
                        call_instr = {
                            "op": "call",
                            "funcs": [func_name],
                            "args": args,
                        }
                        try:
                            func_info = self.lookup_function(func_name)
                        except RuntimeError as e:
                            raise RuntimeError(f"[visitPostfixExpression] Undefined function '{func_name}': {e}")

                        if func_info.return_type is VoidType():
                            self.current_function["instrs"].append(call_instr)
                            return None
                        else:
                            temp_var = self.generate_temp_var()
                            call_instr["dest"] = temp_var
                            call_instr["type"] = func_info.return_type.type_name()
                            self.current_function["instrs"].append(call_instr)
                            return temp_var

                elif ctx.getChild(i).getText() in ['++', '--']:
                    # TODO: not sure whether is correct implementation
                    op = ctx.getChild(i).getText()
                    one_var = self.generate_temp_var()
                    self.current_function["instrs"].append({
                        "op": "const",
                        "dest": one_var,
                        "type": "int",
                        "value": 1
                    })
                    bril_op = 'add' if op == '++' else 'sub'
                    self.current_function["instrs"].append({
                        "op": bril_op,
                        "dest": base_expr,
                        "args": [base_expr, one_var],
                        "type": "int"
                    })

        return base_expr

    def visitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        """
        Handles addition and subtraction.
        """
        if ctx.getChildCount() == 1:
            # Single child, visit recursively
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        op = ctx.getChild(1).getText()  # '+' or '-'
        temp_var = self.generate_temp_var()

        bril_op = "add" if op == "+" else "sub"
        self.current_function["instrs"].append({
            "op": bril_op,
            "dest": temp_var,
            "args": [left, right],
            "type": "int"
        })
        return temp_var

    def visitMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        """
        Handles multiplication, division, and modulo.
        """
        if ctx.getChildCount() == 1:
            # Single child, visit recursively
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        op = ctx.getChild(1).getText()  # '*', '/', or '%'
        temp_var = self.generate_temp_var()

        if op == "%":
            # Generate equivalent mod operation
            # mod(a,b) = a − (a / b) × b
            temp_div = self.generate_temp_var()
            temp_mul = self.generate_temp_var()

            self.current_function["instrs"].append({
                "op": "div",
                "dest": temp_div,
                "args": [left, right],
                "type": "int"
            })
            self.current_function["instrs"].append({
                "op": "mul",
                "dest": temp_mul,
                "args": [temp_div, right],
                "type": "int"
            })
            self.current_function["instrs"].append({
                "op": "sub",
                "dest": temp_var,
                "args": [left, temp_mul],
                "type": "int"
            })
        else:
            # Handle * and /
            bril_op = "mul" if op == "*" else "div"
            self.current_function["instrs"].append({
                "op": bril_op,
                "dest": temp_var,
                "args": [left, right],
                "type": "int"
            })

        return temp_var

    def visitRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        operator = ctx.getChild(1).getText()
        temp_var = self.generate_temp_var()

        bril_op = {
            '<': "lt",
            '>': "gt",
            "<=": "le",
            ">=": "ge"
        }[operator]

        self.current_function["instrs"].append({
            "op": bril_op,
            "dest": temp_var,
            "args": [left, right],
            "type": "bool"
        })
        return temp_var

    def visitEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        operator = ctx.getChild(1).getText()

        if operator == "==":
            temp_var = self.generate_temp_var()
            self.current_function["instrs"].append({
                "op": "eq",
                "dest": temp_var,
                "args": [left, right],
                "type": "bool"
            })
            return temp_var
        elif operator == "!=":
            eq_temp = self.generate_temp_var()
            self.current_function["instrs"].append({
                "op": "eq",
                "dest": eq_temp,
                "args": [left, right],
                "type": "bool"
            })

            not_temp = self.generate_temp_var()
            self.current_function["instrs"].append({
                "op": "not",
                "dest": not_temp,
                "args": [eq_temp],
                "type": "bool"
            })
            return not_temp
        else:
            raise NotImplementedError(f"Unsupported equality operator: {operator}")

    def visitLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        return self._visit_logical_expression(ctx, "and")

    def visitLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        return self._visit_logical_expression(ctx, "or")

    def _visit_logical_expression(self, ctx, bril_op):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        temp_var = self.generate_temp_var()

        self.current_function["instrs"].append({
            "op": bril_op,
            "dest": temp_var,
            "args": [left, right],
            "type": "bool"
        })
        return temp_var

    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        """
        Handles unary expressions for code generation.
        """
        if ctx.postfixExpression():
            return self.visit(ctx.postfixExpression())

        if ctx.unaryOperator():
            operator = ctx.unaryOperator().getText()
            operand = self.visit(ctx.castExpression())
            temp_var = self.generate_temp_var()

            if operator == '+':
                # No operation needed for unary plus
                return operand
            elif operator == '-':
                zero_var = self.generate_temp_var()
                self.current_function["instrs"].append({
                    "op": "const",
                    "dest": zero_var,
                    "type": "int",
                    "value": 0
                })
                temp_var = self.generate_temp_var()
                self.current_function["instrs"].append({
                    "op": "sub",
                    "dest": temp_var,
                    "args": [zero_var, operand],
                    "type": "int"
                })
                return temp_var
            elif operator == '!':
                temp_var = self.generate_temp_var()
                self.current_function["instrs"].append({
                    "op": "not",
                    "dest": temp_var,
                    "args": [operand],
                    "type": "bool"
                })
                return temp_var
            else:
                raise NotImplementedError(f"Unsupported unary operator: {operator}")

        raise NotImplementedError("Unsupported unary expression")

    def visitJumpStatement(self, ctx: CParser.JumpStatementContext):
        """
        Handles jump statements such as return, break, continue, and goto.
        """
        stmt_type = ctx.getChild(0).getText()
        if stmt_type == 'return':
            if ctx.expression():
                # If return has an expression, evaluate it.
                return_value = self.visit(ctx.expression())
                if self.current_function.get("type"):
                    # main function in bril should not return value
                    self.current_function["instrs"].append({
                        "op": "ret",
                        "args": [return_value]
                    })
            else:
                # No return value
                self.current_function["instrs"].append({
                    "op": "ret"
                })
        elif stmt_type in ['break', 'continue']:
            # TODO: Handle 'break' and 'continue' if loops are implemented
            raise NotImplementedError(f"'{stmt_type}' is not yet supported.")
        elif stmt_type == 'goto':
            label = ctx.Identifier().getText() if ctx.Identifier() else self.visit(ctx.unaryExpression())
            self.current_function["instrs"].append({
                "op": "jmp",
                "labels": [label]
            })
        else:
            raise NotImplementedError(f"Unsupported jump statement: {stmt_type}")
