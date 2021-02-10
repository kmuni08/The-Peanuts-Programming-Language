class VarAssignNode:
    def __init__(self, var_name_token, new_value_node):
        self.var_name_token = var_name_token
        self.new_value_node = new_value_node

        self.position_start = self.var_name_token.position_start
        self.position_end = self.new_value_node.position_end
