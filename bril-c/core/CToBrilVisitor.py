from CParser import CParser
from CVisitor import CVisitor

class CToBrilVisitor(CVisitor):
    def __init__(self):
        self.bril_program = {"functions": []}
        self.current_function = None
        self.temp_var_counter = 0

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
        self.current_function = {
            "name": func_name,
            "instrs": []
        }
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
                        # TODO: support Function call
                        print(f"Unsupported function call: {func_name}")
                elif ctx.getChild(i).getText() in ['++', '--']:
                    op = ctx.getChild(i).getText()
                    temp_var = self.generate_temp_var()
                    bril_op = 'add' if op == '++' else 'sub'
                    self.current_function["instrs"].append({
                        "op": bril_op,
                        "dest": temp_var,
                        "args": [base_expr, 1],
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
