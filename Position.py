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

