# CONSTANTS

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


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

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
                result_tokens.append(Token(TT_PLUS))
                self.continue_on()
            elif self.current_char == '-':
                result_tokens.append(Token(TT_MINUS))
                self.continue_on()
            elif self.current_char == '*':
                result_tokens.append(Token(TT_MUL))
                self.continue_on()
            elif self.current_char == '/':
                result_tokens.append(Token(TT_DIV))
                self.continue_on()
            elif self.current_char == '%':
                result_tokens.append(Token(TT_MOD))
                self.continue_on()
            elif self.current_char == '(':
                result_tokens.append(Token(TT_LPAREN))
                self.continue_on()
            elif self.current_char == ')':
                result_tokens.append(Token(TT_RPAREN))
                self.continue_on()
            else:
                # return error by storing char in variable,
                # advance and return empty list and illegalcharacterErr. Return None for err.
                pos_start = self.pos.make_copy()
                char = self.current_char
                self.continue_on()
                return [], IllegalCharacterErr(pos_start, self.pos, "'" + char + "'")
        return result_tokens, None

    def create_number(self):
        num_string = ''
        decimal_count = 0

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
                return Token(TT_INT, int(num_string))
            else:
                return Token(TT_FLOAT, float(num_string))


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
        return result


class IllegalCharacterErr(Error):
    def __init__(self, position_start, position_end, error_content):
        super().__init__(position_start, position_end, 'Illegal Character', error_content)


# POSITION -> keeps track of line number, column number and index
class Position:
    def __init__(self, index, line_number, column_number, file_name, file_text):
        self.index = index
        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.file_text = file_text

    def continue_on(self, current_char):
        self.index += 1
        self.column_number += 1
        if current_char == '\n':
            self.line_number += 1
            self.column_number = 0

        return self

    def make_copy(self):
        return Position(self.index, self.line_number, self.column_number, self.file_name, self.file_text)


# RUN

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.create_tokens()
    return tokens, error
