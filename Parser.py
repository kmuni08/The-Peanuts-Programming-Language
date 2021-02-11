# PARSER
from InvalidSyntaxError import InvalidSyntaxError
from ParseResult import ParseResult
import Constants
from VarAccessNode import VarAccessNode
from VarAssignNode import VarAssignNode
from NodeValue import NodeValue
from UnaryOperationNode import UnaryOperationNode
from BinaryOperationNode import BinaryOperationNode
from IfNode import IfNode
from ForNode import ForNode
from WhileNode import WhileNode
from FuncDefNode import FuncDefNode
from CallNode import CallNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.continue_on()

    def continue_on(self, ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != Constants.TT_EOF:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected '+', '-', '*', '/', '%', '^', '==', '!=', '<', '>', <=', '>=', 'AND' or 'OR'"
            ))
        return res

    def if_expression(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(Constants.TT_KEYWORD, 'IF'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'IF'"
            ))

        res.register_advancement()
        self.continue_on()

        condition = res.doCheck(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(Constants.TT_KEYWORD, 'RETURN'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'RETURN'"
            ))

        res.register_advancement()
        self.continue_on()

        expr = res.doCheck(self.expression())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_token.matches(Constants.TT_KEYWORD, 'EIF'):
            res.register_advancement()
            self.continue_on()

            condition = res.doCheck(self.expression())
            if res.error:
                return res

            if not self.current_token.matches(Constants.TT_KEYWORD, 'RETURN'):
                return res.fail(InvalidSyntaxError(
                    self.current_token.position_start, self.current_token.position_end,
                    f"Expected 'RETURN'"
                ))

            res.register_advancement()
            self.continue_on()

            expr = res.doCheck(self.expression())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_token.matches(Constants.TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.continue_on()

            else_case = res.doCheck(self.expression())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def for_expression(self):
        res = ParseResult()

        if not self.current_token.matches(Constants.TT_KEYWORD, 'FROM'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'FROM'"
            ))

        res.register_advancement()
        self.continue_on()

        if self.current_token.type != Constants.TT_IDENTIFIER:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected identifier"
            ))

        var_name = self.current_token
        res.register_advancement()
        self.continue_on()

        if self.current_token.type != Constants.TT_EQUALS:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.continue_on()

        start_value = res.doCheck(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(Constants.TT_KEYWORD, 'TO'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.continue_on()

        end_value = res.doCheck(self.expression())
        if res.error: return res

        if self.current_token.matches(Constants.TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.continue_on()

            step_value = res.doCheck(self.expression())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_token.matches(Constants.TT_KEYWORD, 'RETURN'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'RETURN'"
            ))

        res.register_advancement()
        self.continue_on()

        body = res.doCheck(self.expression())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expression(self):
        res = ParseResult()

        if not self.current_token.matches(Constants.TT_KEYWORD, 'WHILE'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.continue_on()

        condition = res.doCheck(self.expression())
        if res.error: return res

        if not self.current_token.matches(Constants.TT_KEYWORD, 'RETURN'):
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                f"Expected 'RETURN'"
            ))

        res.register_advancement()
        self.continue_on()

        body = res.doCheck(self.expression())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    # create new atom rule to account for precedence.

    def atom(self):
        result_pr = ParseResult()
        token = self.current_token

        if token.type in (Constants.TT_INT, Constants.TT_FLOAT):
            result_pr.register_advancement()
            self.continue_on()
            return result_pr.success(NodeValue(token))
        elif token.type == Constants.TT_IDENTIFIER:
            result_pr.register_advancement()
            self.continue_on()
            return result_pr.success(VarAccessNode(token))
        elif token.type == Constants.TT_LPAREN:
            result_pr.register_advancement()
            self.continue_on()
            expression = result_pr.doCheck(self.expression())
            if result_pr.error:
                return result_pr
            if self.current_token.type == Constants.TT_RPAREN:
                result_pr.register_advancement()
                self.continue_on()
                return result_pr.success(expression)
            else:
                return result_pr.fail(
                    InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
                                       "Expected ')'"))

        elif token.matches(Constants.TT_KEYWORD, 'IF'):
            if_expression = result_pr.doCheck(self.if_expression())
            if result_pr.error:
                return result_pr
            return result_pr.success(if_expression)

        elif token.matches(Constants.TT_KEYWORD, 'FROM'):
            for_expression = result_pr.doCheck(self.for_expression())
            if result_pr.error:
                return result_pr
            return result_pr.success(for_expression)

        elif token.matches(Constants.TT_KEYWORD, 'WHILE'):
            while_expression = result_pr.doCheck(self.while_expression())
            if result_pr.error:
                return result_pr
            return result_pr.success(while_expression)

        elif token.matches(Constants.TT_KEYWORD, 'BLOCKHEAD'):
            function_definition = result_pr.doCheck(self.function_definition())
            if result_pr.error:
                return result_pr
            return result_pr.success(function_definition)

        return result_pr.fail(InvalidSyntaxError(
            token.position_start, token.position_end,
            "Expected int, float, identifier, '+', '-', '(', 'IF', 'FOR', 'WHILE', or 'BLOCKHEAD' "
        ))

    def power(self):
        return self.binary_operation(self.call, (Constants.TT_POWER,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.doCheck(self.atom())
        if res.error:
            return res
        if self.current_token.type == Constants.TT_LPAREN:
            res.register_advancement()
            self.continue_on()
            arg_nodes = []

            if self.current_token.type == Constants.TT_RPAREN:
                res.register_advancement()
                self.continue_on()
            else:
                arg_nodes.append(res.doCheck(self.expression()))
                if res.error:
                    return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                                       self.current_token.position_end,
                                                       "Expected ')', 'LET', 'IF', 'FOR', 'WHILE', 'BLOCKHEAD', int, "
                                                       "float, identifier,'+', '-', '(' or 'NOT'"
                                                       ))
                while self.current_token.type == Constants.TT_COMMA:
                    res.register_advancement()
                    self.continue_on()

                    arg_nodes.append(res.doCheck(self.expression()))
                    if res.error:
                        return res

                if self.current_token.type != Constants.TT_RPAREN:
                    return res.fail(InvalidSyntaxError(
                        self.current_token.position_start, self.current_token.position_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.continue_on()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    # look for int or float and return Number node.
    def factor(self):
        result_pr = ParseResult()
        token = self.current_token

        if token.type in (Constants.TT_PLUS, Constants.TT_MINUS):
            result_pr.register_advancement()
            self.continue_on()
            factor = result_pr.doCheck(self.factor())
            if result_pr.error:
                return result_pr
            return result_pr.success(UnaryOperationNode(token, factor))

        return self.power()

    # look for factor, see if token in MULT or DIV or MOD then look for another factor.
    def term(self):
        return self.binary_operation(self.factor, (Constants.TT_MUL, Constants.TT_DIV, Constants.TT_MOD))

    def expression(self):
        res = ParseResult()
        if self.current_token.matches(Constants.TT_KEYWORD, 'LET'):
            # new rule
            res.register_advancement()
            self.continue_on()

            if self.current_token.type != Constants.TT_IDENTIFIER:
                return res.fail(InvalidSyntaxError(
                    self.current_token.position_start, self.current_token.position_end, "Expected identifier"
                ))

            var_name = self.current_token
            res.register_advancement()
            self.continue_on()

            if self.current_token.type != Constants.TT_EQUALS:
                return res.fail(InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
                                                   "Expected '='"))
            res.register_advancement()
            self.continue_on()
            expr = res.doCheck(self.expression())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))
        node = res.doCheck(self.binary_operation(self.comp_expr, ((Constants.TT_KEYWORD, "AND"),
                                                                  (Constants.TT_KEYWORD, "OR"))))
        if res.error:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected 'LET', 'IF', 'FOR', 'WHILE', 'BLOCKHEAD', int, float, identifier, '+', '-' or '(' or 'NOT' "
            ))

        return res.success(node)

    def arithmetic_expr(self):
        return self.binary_operation(self.term, (Constants.TT_PLUS, Constants.TT_MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.current_token.matches(Constants.TT_KEYWORD, 'NOT'):
            operation_token = self.current_token
            res.register_advancement()
            self.continue_on()

            node = res.doCheck(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOperationNode(operation_token, node))

        node = res.doCheck(self.binary_operation(self.arithmetic_expr, (Constants.TT_EE, Constants.TT_NE,
                                                                        Constants.TT_LT, Constants.TT_LTE,
                                                                        Constants.TT_GT, Constants.TT_GTE)))
        if res.error:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected int, float, identifier, '+', '-', '(', or 'NOT' "
            ))

        return res.success(node)

    def function_definition(self):
        res = ParseResult()

        if not self.current_token.matches(Constants.TT_KEYWORD, 'BLOCKHEAD'):
            return res.fail(InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
                                               f"Expected 'BLOCKHEAD'"))
        res.register_advancement()
        self.continue_on()

        if self.current_token.type == Constants.TT_IDENTIFIER:
            var_name_token = self.current_token
            res.register_advancement()
            self.continue_on()
            if self.current_token.type != Constants.TT_LPAREN:
                return res.fail(InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
                                                   f"Expected '('"))
        else:
            var_name_token = None
            if self.current_token.type != Constants.TT_LPAREN:
                return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                                   self.current_token.position_end, f"Expected identifier or '('"))

        res.register_advancement()
        self.continue_on()
        arg_name_tokens = []

        if self.current_token.type == Constants.TT_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            res.register_advancement()
            self.continue_on()

            while self.current_token.type == Constants.TT_COMMA:
                res.register_advancement()
                self.continue_on()

                if self.current_token.type != Constants.TT_IDENTIFIER:
                    return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                                       self.current_token.position_end,
                                                       f"Expected identifier"))
                arg_name_tokens.append(self.current_token)
                res.register_advancement()
                self.continue_on()

            if self.current_token.type != Constants.TT_RPAREN:
                return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                                   self.current_token.position_end, f"Expected ',' or ')'"))
        else:
            if self.current_token.type != Constants.TT_RPAREN:
                return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                                   self.current_token.position_end,
                                                   f"Expected identifier or ')'"))
        res.register_advancement()
        self.continue_on()

        if self.current_token.type != Constants.TT_ARROW:
            return res.fail(InvalidSyntaxError(self.current_token.position_start,
                                               self.current_token.position_end,
                                               f"Expected '->'"))

        res.register_advancement()
        self.continue_on()
        node_to_return = res.doCheck(self.expression())
        if res.error:
            return res

        return res.success(FuncDefNode(
            var_name_token,
            arg_name_tokens,
            node_to_return
        ))

    # shared by term and expression
    def binary_operation(self, func_1, operations, func_2=None):
        if func_2 is None:
            func_2 = func_1

        result_pr = ParseResult()
        left = result_pr.doCheck(func_1())

        if result_pr.error:
            return result_pr

        while self.current_token.type in operations or (
                self.current_token.type, self.current_token.value) in operations:
            operator_token = self.current_token
            result_pr.register_advancement()
            self.continue_on()
            right = result_pr.doCheck(func_2())
            if result_pr.error:
                return result_pr
            left = BinaryOperationNode(left, operator_token, right)
        return result_pr.success(left)
