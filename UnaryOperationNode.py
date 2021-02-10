class UnaryOperationNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node
        self.position_start = self.operator_token.position_start
        self.position_end = node.position_end

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'
