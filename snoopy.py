# CONSTANTS
from SymbolTable import SymbolTable
from Number import Number
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from Context import Context

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("FALSE", Number(0))
global_symbol_table.set("TRUE", Number(1))


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
    # interpreter = Interpreter()
    # context = Context('<program>')
    # context.symbol_table = global_symbol_table
    # result = interpreter.visitNode(ast.node, context)

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visitNode(ast.node, context)

    return result.value, result.error
