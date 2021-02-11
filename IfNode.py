class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.position_start = self.cases[0][0].position_start
        self.position_end = (self.else_case or self.cases[len(self.cases) - 1][0]).position_end
