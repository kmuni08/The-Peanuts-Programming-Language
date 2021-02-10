
class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.position_start = self.var_name_token.position_start
        self.position_end = self.var_name_token.position_end