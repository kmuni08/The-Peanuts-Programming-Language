import string

DIGITS = '0123456789'
# all letters from A-Z
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_POWER = 'POWER'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_EQUALS = 'EQUALS'
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_EOF = 'EOF'

KEYWORDS = [
    'LET',
    'AND',
    'OR',
    'NOT',
    'IF',
    'RETURN',
    'EIF',
    'ELSE',
    'FROM',
    'TO',
    'STEP',
    'WHILE'
]