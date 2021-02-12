from Token import Token
from Position import Position
import Constants
from IllegalCharacterErr import IllegalCharacterErr
from ExpectedCharError import ExpectedCharError


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
            elif self.current_char == '"':
                result_tokens.append(self.create_string())
            elif self.current_char == '+':
                result_tokens.append(Token(Constants.TT_PLUS, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '-':
                # result_tokens.append(Token(Constants.TT_MINUS, position_start=self.pos))
                # self.continue_on()
                result_tokens.append(self.make_minus_or_arrow())
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
            elif self.current_char == '(':
                result_tokens.append(Token(Constants.TT_LPAREN, position_start=self.pos))
                self.continue_on()
            elif self.current_char == ')':
                result_tokens.append(Token(Constants.TT_RPAREN, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '[':
                result_tokens.append(Token(Constants.TT_LSQUARE, position_start=self.pos))
                self.continue_on()
            elif self.current_char == ']':
                result_tokens.append(Token(Constants.TT_RSQUARE, position_start=self.pos))
                self.continue_on()
            elif self.current_char == '!':
                # check if next char is =, if so create make_not_equals() token.
                token, error = self.make_not_equals()
                if error:
                    return [], error
                result_tokens.append(token)
            elif self.current_char == '=':
                # make single equals if 1 eq or double equals if 2 eq.
                result_tokens.append(self.make_equals())
            elif self.current_char == '<':
                result_tokens.append(self.make_less_than())
            elif self.current_char == '>':
                result_tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                result_tokens.append(Token(Constants.TT_COMMA, position_start=self.pos))
                self.continue_on()
            else:
                # return error by storing char in variable,
                # advance and return empty list and IllegalCharacterErr. Return None for err.
                pos_start = self.pos.make_copy()
                char = self.current_char
                self.continue_on()
                return [], IllegalCharacterErr(pos_start, self.pos, "'" + char + "' ")

        result_tokens.append(Token(Constants.TT_EOF, position_start=self.pos))
        return result_tokens, None

    def create_number(self):
        num_string = ''
        dot_count = 0
        pos_start = self.pos.make_copy()

        while self.current_char is not None and self.current_char in Constants.DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num_string += self.current_char
            self.continue_on()

        if dot_count == 0:
            return Token(Constants.TT_INT, int(num_string), pos_start, self.pos)
        else:
            return Token(Constants.TT_FLOAT, float(num_string), pos_start, self.pos)

    def create_identifier(self):
        id_str = ''
        position_start = self.pos.make_copy()

        while self.current_char is not None and self.current_char in Constants.LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.continue_on()

        # Built id string... determine whether to create identifier or keyword token.
        token_type = Constants.TT_KEYWORD if id_str in Constants.KEYWORDS else Constants.TT_IDENTIFIER
        return Token(token_type, id_str, position_start, self.pos)

    def make_not_equals(self):
        position_start = self.pos.make_copy()
        # current character is !
        self.continue_on()

        if self.current_char == '=':
            self.continue_on()
            return Token(Constants.TT_NE, position_start=position_start, position_end=self.pos), None

        self.continue_on()
        return None, ExpectedCharError(position_start, self.pos, "'=' (after '!') ")

    def make_equals(self):
        token_type = Constants.TT_EQUALS
        position_start = self.pos.make_copy()
        self.continue_on()

        if self.current_char == '=':
            self.continue_on()
            token_type = Constants.TT_EE

        return Token(token_type, position_start=position_start, position_end=self.pos)

    def make_less_than(self):
        token_type = Constants.TT_LT
        position_start = self.pos.make_copy()
        self.continue_on()

        if self.current_char == '=':
            self.continue_on()
            token_type = Constants.TT_LTE

        return Token(token_type, position_start=position_start, position_end=self.pos)

    def make_greater_than(self):
        token_type = Constants.TT_GT
        position_start = self.pos.make_copy()
        self.continue_on()

        if self.current_char == '=':
            self.continue_on()
            token_type = Constants.TT_GTE

        return Token(token_type, position_start=position_start, position_end=self.pos)

    def make_minus_or_arrow(self):
        token_type = Constants.TT_MINUS
        position_start = self.pos.make_copy()
        self.continue_on()

        if self.current_char == '>':
            self.continue_on()
            token_type = Constants.TT_ARROW

        return Token(token_type, position_start=position_start, position_end=self.pos)

    def create_string(self):
        string = ''
        position_start = self.pos.make_copy()
        escape_character = False
        self.continue_on()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char is not None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                # check to see if current_char is a backslash
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.continue_on()
            escape_character = False

        self.continue_on()
        return Token(Constants.TT_STRING, string, position_start, self.pos)

