from Number import Number
from Value import Value


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def add_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def mul_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.position_start, self.position_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'"{self.value}"'
