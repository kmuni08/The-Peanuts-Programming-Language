from Token import Token
from Position import Position
import Constants
from IllegalCharacterErr import IllegalCharacterErr


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
            elif self.current_char in Constants.DIGITS:
                # since there could be more than one digit, we will make function to create numbers
                result_tokens.append(self.create_number())
            elif self.current_char in Constants.LETTERS:
                result_tokens.append(self.create_identifier())
            elif self.current_char == '+':
                result_tokens.append(Token(Constants.TT_PLUS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '-':
                result_tokens.append(Token(Constants.TT_MINUS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '*':
                result_tokens.append(Token(Constants.TT_MUL, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '/':
                result_tokens.append(Token(Constants.TT_DIV, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '%':
                result_tokens.append(Token(Constants.TT_MOD, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '^':
                result_tokens.append(Token(Constants.TT_POWER, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '=':
                result_tokens.append(Token(Constants.TT_EQUALS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '(':
                result_tokens.append(Token(Constants.TT_LPAREN, position_start=self.pos))
                self.continue_on()
            elif self.current_char == ')':
                result_tokens.append(Token(Constants.TT_RPAREN, position_start=self.pos))
                self.continue_on()
            else:
                # return error by storing char in variable,
                # advance and return empty list and illegalcharacterErr. Return None for err.
                pos_start = self.pos.make_copy()
                char = self.current_char
                self.continue_on()
                return [], IllegalCharacterErr(pos_start, self.pos, "'" + char + "' ")

        result_tokens.append(Token(Constants.TT_EOF, position_start=self.pos))
        return result_tokens, None

    def create_number(self):
        num_string = ''
        decimal_count = 0
        position_start = self.pos.make_copy()

        # if there is a number with decimal, it's a double.

        while self.current_char is not None and self.current_char in Constants.DIGITS + '.':
            if self.current_char == ".":
                if decimal_count == 1:
                    break
                decimal_count += 1
            num_string += self.current_char
            self.continue_on()

            print(Token(Constants.TT_INT, int(num_string), position_start, self.pos))
            if decimal_count == 0:
                return Token(Constants.TT_INT, int(num_string), position_start, self.pos)
            else:
                return Token(Constants.TT_FLOAT, float(num_string), position_start, self.pos)

    def create_identifier(self):
        id_str = ''
        position_start = self.pos.make_copy()

        while self.current_char is not None and self.current_char in Constants.LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.continue_on()

        # Built id string... determine whether to create identifier or keyword token.
        token_type = Constants.TT_KEYWORD if id_str in Constants.KEYWORDS else Constants.TT_IDENTIFIER
        return Token(token_type, id_str, position_start, self.pos)
