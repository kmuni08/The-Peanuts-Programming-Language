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


class RunTimeError(Error):
    def __init__(self, position_start, position_end, error_content, context):
        super().__init__(position_start, position_end, 'Run Time Error', error_content)
        self.context = context

    def __str__(self):
        result = self.generate_traceback()
        result += f'{self.error_message}: {self.error_content}'
        result += '\n\n' + string_with_arrows(self.position_start.file_text, self.position_start, self.position_end)
        return result

    def generate_traceback(self):
        result = ''
        position = self.position_start
        ctx = self.context
        while ctx:
            result = f' File {position.file_name}, line {str(position.line_number + 1)}, in {ctx.display_name} \n' \
                     + result
            position = ctx.parent_entry_position
            ctx = ctx.parent

        return 'Traceback (most recent call last ):\n' + result


# POSITION -> keeps track of line number, column number and index
class Position:
    def __init__(self, index, line_number, column_number, file_name, file_text):
        self.index = index
        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.file_text = file_text

    def continue_on(self, current_char=None):
        self.index += 1
        self.column_number += 1
        if current_char == '\n':
            self.line_number += 1
            self.column_number = 0

        return self

    def make_copy(self):
        return Position(self.index, self.line_number, self.column_number, self.file_name, self.file_text)


# NODES
class NodeValue:
    # takes in number token if int or float.
    def __init__(self, token):
        self.token = token
        self.position_start = self.token.position_start
        self.position_end = self.token.position_end

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.position_start = self.left_node.position_start
        self.position_end = self.right_node.position_end

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'


class UnaryOperationNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        self.position_start = self.operator_token.position_start
        self.position_end = node.position_end

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'


# Instead of returning a Node in each function, we'll return
# ParseResult, it'll check if there are any errors

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    # take in ParseResult or node.
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
            return result_pr.success(NodeValue(token))
        elif token.type == TT_LPAREN:
            result_pr.doCheck(self.continue_on())
            expression = result_pr.doCheck(self.expression())
            if result_pr.error:
                return result_pr
            if self.current_token.type == TT_RPAREN:
                result_pr.doCheck(self.continue_on())
                return result_pr.success(expression)
            else:
                return result_pr.fail(
                    InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end,
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


# keeps track of result and error if any. Like the Parser Result class.
class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


# NUMBER class to store numbers and operate on other numbers

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start, other.position_end,
                    'Division by zero ',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def mod_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


# INTERPRETER

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

        print("Hello", node.operator_token.type)
        if node.operator_token.type == TT_PLUS:
            result, error = left.add_to(right)
        elif node.operator_token.type == TT_MINUS:
            result, error = left.sub_by(right)
        elif node.operator_token.type == TT_MUL:
            result, error = left.mul_by(right)
        elif node.operator_token.type == TT_DIV:
            result, error = left.div_by(right)
        elif node.operator_token.type == TT_MOD:
            result, error = left.mod_by(right)

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

        if node.operator_token.type == TT_MINUS:
            number, error = number.mul_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.position_start, node.position_end))


# Create CONTEXT Class for updating context of where error is coming from.
# holds current context of the program. (Functions or entire program)
# display name = error, function name or program
# parent = parent of divide_by_zero would be function name
# parent_entry_position: position where context changes.
class Context:
    def __init__(self, display_name, parent=None, parent_entry_position=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position


# RUN
def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()
    if error:
        return None, error
    # GENERATE AST
    parser = Parser(tokens)
    ast = parser.parse()

    # Create Instance of Interpreter
    if ast.error:
        return None, ast.error
    # Run Program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visitNode(ast.node, context)

    return result.value, result.error
