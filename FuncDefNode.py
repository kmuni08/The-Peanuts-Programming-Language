class FuncDefNode:
    # var_name_token -> name of function, none if function in anonymous.
    # names for args
    # body_node is evaluated when function is called.
    def __init__(self, var_name_token, arg_name_tokens, body_node):
        self.var_name_token = var_name_token
        self.arg_name_tokens = arg_name_tokens
        self.body_node = body_node

        if self.var_name_token:
            self.position_start = self.var_name_token.position_start
        elif len(self.arg_name_tokens) > 0:
            self.position_start = self.arg_name_tokens[0].position_start
        else:
            self.position_start = self.body_node.position_start

        self.position_end = self.body_node.position_end
