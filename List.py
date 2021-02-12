from Value import Value
from Number import Number


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def add_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def sub_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RuntimeError(
                    other.position_start, other.position_end,
                    'Element at this index could not be removed from the list, because'
                    'index is out of bounds. ',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def mul_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def div_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RuntimeError(
                    other.position_start, other.position_end,
                    'Element at this index could not be retrieved from the list, because'
                    'index is out of bounds. ',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements[:])
        copy.set_pos(self.position_start, self.position_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'
