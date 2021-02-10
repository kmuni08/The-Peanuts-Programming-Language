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
        self.symbol_table = None
