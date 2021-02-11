# NUMBER class to store numbers and operate on other numbers
from RunTimeError import RunTimeError


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start, other.position_end,
                    'Division by zero ',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def mod_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None

    def pow_of(self, other):
        if isinstance(other, Number):
            return Number(pow(self.value, other.value)).set_context(self.context), None

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value != other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value < other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value > other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value >= other.value)).set_context(self.context), None

    def and_by(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value and other.value)).set_context(self.context), None

    def or_by(self, other):
        if isinstance(other, Number):
            return Number(bool(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.position_start, self.position_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)
