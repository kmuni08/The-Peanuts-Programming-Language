# PARSER
from InvalidSyntaxError import InvalidSyntaxError
from ParseResult import ParseResult
import Constants
from VarAccessNode import VarAccessNode
from VarAssignNode import VarAssignNode
from NodeValue import NodeValue
from UnaryOperationNode import UnaryOperationNode
from BinaryOperationNode import BinaryOperationNode


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
                "Expected '+', '-', '*', '/', '%', or '^' "
            ))
        return res

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
        return result_pr.fail(InvalidSyntaxError(
            self.current_token.position_start, self.current_token.position_end,
            "Expected int, float, identifier, '+', '-', or '(' "
        ))

    def power(self):
        return self.binary_operation(self.atom, (Constants.TT_POWER,), self.factor)

    # look for int or float and return Number node.
    def factor(self):
        result_pr = ParseResult()
        token = self.current_token

        if token.type in (Constants.TT_PLUS, Constants.TT_MINUS):
            result_pr.doCheck(self.continue_on())
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
        node = res.doCheck(self.binary_operation(self.term, (Constants.TT_PLUS, Constants.TT_MINUS)))
        if res.error:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected 'LET', int, float, identifier, '+', '-' or '(' "
            ))

        return res.success(node)

    # shared by term and expression
    def binary_operation(self, func_1, operations, func_2=None):
        if func_2 is None:
            func_2 = func_1

        result_pr = ParseResult()
        left = result_pr.doCheck(func_1())

        if result_pr.error:
            return result_pr

        while self.current_token.type in operations:
            operator_token = self.current_token
            result_pr.register_advancement()
            self.continue_on()
            right = result_pr.doCheck(func_2())
            if result_pr.error:
                return result_pr
            left = BinaryOperationNode(left, operator_token, right)
        return result_pr.success(left)
