# INTERPRETER
from Number import Number
import Constants
from RunTimeResult import RunTimeResult
from Value import Value
from Context import Context
from SymbolTable import SymbolTable
from RunTimeError import RunTimeError
from String import String
from List import List

class Interpreter:
    # takes in node to process, then visit child nodes. Want to determine
    # what function to call based on node.
    def visitNode(self, node, context):
        function_name = f'visit_{type(node).__name__}'
        function = getattr(self, function_name, self.no_visit_function)
        return function(node, context)

    def no_visit_function(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    # Number node function
    def visit_NodeValue(self, node, context):
        # update the Node class to account for position_start and position_end
        return RunTimeResult().success(
            Number(node.token.value).set_context(context).set_pos(node.position_start, node.position_end))

    def visit_VarAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RunTimeError(node.position_start, node.position_end, f"'{var_name}' is not defined",
                                            context))
        value = value.copy().set_pos(node.position_start, node.position_end)
        return res.success(value)

    def visit_IfNode(self, node, context):
        res = RunTimeResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visitNode(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visitNode(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visitNode(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RunTimeResult()

        elements = []

        start_value = res.register(self.visitNode(node.start_value_node, context))
        if res.error:
            return res

        end_value = res.register(self.visitNode(node.end_value_node, context))
        if res.error:
            return res

        if node.step_value_node:
            step_value = res.register(self.visitNode(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_token.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visitNode(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.position_start, node.position_end)
        )

    def visit_WhileNode(self, node, context):
        res = RunTimeResult()
        elements = []

        while True:
            condition = res.register(self.visitNode(node.condition_node, context))
            if res.error:
                return res

            if not condition.is_true():
                break

            elements.append(res.register(self.visitNode(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.position_start, node.position_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RunTimeResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        print(func_name)
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.position_start,
                                                                                            node.position_end)
        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RunTimeResult()
        args = []

        value_to_call = res.register(self.visitNode(node.node_to_call, context))
        if res.error:
            return res
        value_to_call = value_to_call.copy().set_pos(node.position_start, node.position_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visitNode(arg_node, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res
        return res.success(return_value)

    def visit_StringNode(self, node, context):
        return RunTimeResult().success(
            String(node.token.value).set_context(context).set_pos(node.position_start, node.position_end)
        )

    def visit_ListNode(self, node, context):
        res = RunTimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visitNode(element_node, context)))
            if res.error:
                return res
        return res.success(
            List(elements).set_context(context).set_pos(node.position_start, node.position_end)
        )

    def visit_VarAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visitNode(node.new_value_node, context))

        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    # Binary Operator Node
    def visit_BinaryOperationNode(self, node, context):
        # calls the root node for now. Want to call left and right nodes
        res = RunTimeResult()
        left = res.register(self.visitNode(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visitNode(node.right_node, context))
        if res.error:
            return res
        if node.operator_token.type == Constants.TT_PLUS:
            result, error = left.add_to(right)
        elif node.operator_token.type == Constants.TT_MINUS:
            result, error = left.sub_by(right)
        elif node.operator_token.type == Constants.TT_MUL:
            result, error = left.mul_by(right)
        elif node.operator_token.type == Constants.TT_DIV:
            result, error = left.div_by(right)
        elif node.operator_token.type == Constants.TT_MOD:
            result, error = left.mod_by(right)
        elif node.operator_token.type == Constants.TT_POWER:
            result, error = left.pow_of(right)
        elif node.operator_token.type == Constants.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.operator_token.type == Constants.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.operator_token.type == Constants.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.operator_token.type == Constants.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.operator_token.type == Constants.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.operator_token.type == Constants.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.operator_token.matches(Constants.TT_KEYWORD, 'AND'):
            result, error = left.and_by(right)
        elif node.operator_token.matches(Constants.TT_KEYWORD, 'OR'):
            result, error = left.or_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.position_start, node.position_end))

    # Unary Operator Node
    def visit_UnaryOperationNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visitNode(node.node, context))

        if res.error:
            return res

        error = None

        if node.operator_token.type == Constants.TT_MINUS:
            number, error = number.mul_by(Number(-1))
        elif node.operator_token.type.matches(Constants.TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.position_start, node.position_end))


class Function(Value):
    def __init__(self, func_name, body_node, arg_names):
        super().__init__()
        self.func_name = func_name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RunTimeResult()
        # make interpreter a static class
        interpreter = Interpreter()
        new_context = Context(self.func_name, self.context, self.position_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RunTimeError(
                self.position_start, self.position_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.func_name}'",
                self.context
            ))

        if len(args) < len(self.arg_names):
            return res.failure(RunTimeError(
                self.position_start, self.position_end,
                f"{len(self.arg_names) - len(args)} too few args passed into '{self.func_name}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visitNode(self.body_node, new_context))
        if res.error:
            return res
        return res.success(value)

    def copy(self):
        copy = Function(self.func_name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.position_start, self.position_end)
        return copy

    def __repr__(self):
        return f"<function {self.func_name}>"

