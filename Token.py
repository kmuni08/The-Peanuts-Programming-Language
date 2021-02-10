# TOKEN:

class Token:
    def __init__(self, type_, value=None, position_start=None, position_end=None):
        self.type = type_
        self.value = value

        if position_start:
            self.position_start = position_start.make_copy()
            self.position_end = position_start.make_copy()
            self.position_end.continue_on()

        if position_end:
            self.position_end = position_end.make_copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    # how we want this to print in the terminal.
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'

        # if it doesn't have value, print the type.
        return f'{self.type}'
