# INTERPRETER
from RunTimeResult import RunTimeResult
from Number import Number
from RunTimeError import RunTimeError
import Constants


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
