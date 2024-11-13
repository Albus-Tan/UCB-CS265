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
            return ctx.Identifier().getText()
        elif ctx.Constant():
            temp_var = self.generate_temp_var()
            # TODO: support more types
            self.current_function["instrs"].append({
                "op": "const",
                "dest": temp_var,
                "type": "int",
                "value": int(ctx.Constant().getText())
            })
            return temp_var
        elif ctx.expression():
            return self.visit(ctx.expression())
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

        expr_result = self.visit(initializer.assignmentExpression())
        # TODO: support more types
        self.current_function["instrs"].append({
            "op": "id",
            "dest": var_name,
            "type": "int",
            "args": [expr_result]
        })

    def visitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        if ctx.getChildCount() == 3 and ctx.assignmentOperator():
            var_name = ctx.getChild(0).getText()
            operator = ctx.getChild(1).getText()
            right_expr_result = self.visit(ctx.getChild(2))

            if operator == "=":
                # TODO: support more types
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
                    "%=": "mod",
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



