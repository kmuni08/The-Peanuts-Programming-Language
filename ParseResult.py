# Instead of returning a Node in each function, we'll return
# ParseResult, it'll check if there are any errors

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    # Only for continuing on:
    def register_advancement(self):
        self.advance_count += 1

    # take in ParseResult or node. Pass Parse Results
    def doCheck(self, result):
        self.advance_count += result.advance_count
        if result.error:
            self.error = result.error
        return result.node

    def success(self, node):
        self.node = node
        return self

    def fail(self, error):
        # should override if we haven't advanced since.
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
