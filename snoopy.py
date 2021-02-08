# CONSTANTS
from string_with_arrows import *

DIGITS = '0123456789'

# TOKEN:

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'


class Token:
    def __init__(self, type_, value=None, position_start=None, position_end=None):
        self.type = type_
        self.value = value

        if position_start:
            self.position_start = position_start.make_copy()
            self.position_end = position_start.make_copy()
            self.position_end.continue_on()

        if position_end:
            self.position_end = position_end

    # how we want this to print in the terminal.
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'

        # if it doesn't have value, print the type.
        return f'{self.type}'


# Lexer class

class Lexer:
    # take in text we'd be processing. Keep track of position and character
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        # we call continue_on immediately so we start at 0.
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.continue_on()

    def continue_on(self):
        self.pos.continue_on(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def create_tokens(self):
        result_tokens = []
        while self.current_char is not None:
            # ignore whitespaces and tabs
            if self.current_char in ' \t':
                self.continue_on()
            elif self.current_char in DIGITS:
                # since there could be more than one digit, we will make function to create numbers
                result_tokens.append(self.create_number())
            elif self.current_char == '+':
                result_tokens.append(Token(TT_PLUS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '-':
                result_tokens.append(Token(TT_MINUS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '*':
                result_tokens.append(Token(TT_MUL, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '/':
                result_tokens.append(Token(TT_DIV, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '%':
                result_tokens.append(Token(TT_MOD, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '(':
                result_tokens.append(Token(TT_LPAREN, position_start=self.pos))
                self.continue_on()
            elif self.current_char == ')':
                result_tokens.append(Token(TT_RPAREN, position_start=self.pos))
                self.continue_on()
            else:
                # return error by storing char in variable,
                # advance and return empty list and illegalcharacterErr. Return None for err.
                pos_start = self.pos.make_copy()
                char = self.current_char
                self.continue_on()
                return [], IllegalCharacterErr(pos_start, self.pos, "'" + char + "' ")

        result_tokens.append(Token(TT_EOF, position_start=self.pos))
        return result_tokens, None

    def create_number(self):
        num_string = ''
        decimal_count = 0
        position_start = self.pos.make_copy()

        # if there is a number with decimal, it's a double.

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == ".":
                if decimal_count == 1:
                    break
                decimal_count += 1
                num_string += '.'
            else:
                num_string += self.current_char
            self.continue_on()

            if decimal_count == 0:
                return Token(TT_INT, int(num_string), position_start, self.pos)
            else:
                return Token(TT_FLOAT, float(num_string), position_start, self.pos)


# CUSTOM ERROR CLASS

class Error:
    def __init__(self, position_start, position_end, error_message, error_content):
        self.position_start = position_start
        self.position_end = position_end
        self.error_message = error_message
        self.error_content = error_content

    def __str__(self):
        result = f'{self.error_message}: {self.error_content}'
        result += f'File {self.position_start.file_name}, line {self.position_start.line_number + 1}'
        result += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end)
        return result


class IllegalCharacterErr(Error):
    def __init__(self, position_start, position_end, error_content):
        super().__init__(position_start, position_end, 'Illegal Character', error_content)


class InvalidSyntaxError(Error):
    def __init__(self, position_start, position_end, error_content=''):
        super().__init__(position_start, position_end, 'Illegal Syntax', error_content)


# POSITION -> keeps track of line number, column number and index
class Position:
    def __init__(self, index, line_number, column_number, file_name, file_text):
        self.index = index
        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.file_text = file_text

    def continue_on(self, current_char = None):
        self.index += 1
        self.column_number += 1
        if current_char == '\n':
            self.line_number += 1
            self.column_number = 0

        return self

    def make_copy(self):
        return Position(self.index, self.line_number, self.column_number, self.file_name, self.file_text)


# NODES
class NumberNode:
    # takes in number token if int or float.
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'


class UnaryOperationNode:
    def __init__(self, operation_token, node):
        self.operation_token = operation_token
        self.node = node

    def __repr__(self):
        return f'({self.operation_token}, {self.node})'


# Instead of returning a Node in each function, we'll return
# ParseResult, it'll check if there are any errors

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def doCheck(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result

    def success(self, node):
        self.node = node
        return self

    def fail(self, error):
        self.error = error
        return self


# PARSER
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
        if not res.error and self.current_token.type != TT_EOF:
            return res.fail(InvalidSyntaxError(
                self.current_token.position_start, self.current_token.position_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    # look for int or float and return Number node.
    def factor(self):
        result_pr = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            result_pr.doCheck(self.continue_on())
            factor = result_pr.doCheck(self.factor())
            if result_pr.error:
                return result_pr
            return result_pr.success(UnaryOperationNode(token, factor))
        elif token.type in (TT_INT, TT_FLOAT):
            result_pr.doCheck(self.continue_on())
            return result_pr.success(NumberNode(token))
        elif token.type == TT_LPAREN:
            result_pr.doCheck(self.continue_on())
            expression = result_pr.doCheck(self.expression())
            if result_pr.error:
                return result_pr
            if self.current_token.type == TT_RPAREN:
                result_pr.doCheck(self.continue_on())
                return result_pr.success(expression)
            else:
                return result_pr.fail(InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
                                                   "Expected ')'"))

        return result_pr.fail(InvalidSyntaxError(
            token.position_start, token.postion_end,
            "Expected int or float "
        ))

    # look for factor, see if token in MULT or DIV or MOD then look for another factor.
    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def expression(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

    # shared by term and expression
    def binary_operation(self, func, operations):
        result_pr = ParseResult()
        left = result_pr.doCheck(func())
        if result_pr.error:
            return result_pr

        while self.current_token.type in operations:
            operator_token = self.current_token
            result_pr.doCheck(self.continue_on())
            right = result_pr.doCheck(func())
            if result_pr.error:
                return result_pr
            left = BinaryOperationNode(left, operator_token, right)
        return result_pr.success(left)


# RUN
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()

    if error:
        return None, error
    # GENERATE AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
