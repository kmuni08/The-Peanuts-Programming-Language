from Value import Value
from Context import Context
from SymbolTable import SymbolTable
from RunTimeError import RunTimeError
from RunTimeResult import RunTimeResult

class BaseFunction(Value):
    def __init__(self, func_name):
        super().__init__()
        self.func_name = func_name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.func_name, self.context, self.position_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RunTimeResult()
        if len(args) > len(arg_names):
            return res.failure(RunTimeError(
                self.position_start, self.position_end,
                f"{len(args) - len(arg_names)} too many args passed into '{self.func_name}'",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RunTimeError(
                self.position_start, self.position_end,
                f"{len(arg_names) - len(args)} too few args passed into '{self.func_name}'",
                self.context
            ))

        return res.success(None)

