class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.position_start = self.node_to_call.position_start

        if len(self.arg_nodes) > 0:
            self.position_end = self.arg_nodes[len(self.arg_nodes) - 1].position_end
        else:
            self.position_end = self.node_to_call.position_end
