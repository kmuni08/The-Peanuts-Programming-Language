class StringNode:
    # takes in string.
    def __init__(self, token):
        self.token = token
        self.position_start = self.token.position_start
        self.position_end = self.token.position_end

    def __repr__(self):
        return f'{self.token}'
