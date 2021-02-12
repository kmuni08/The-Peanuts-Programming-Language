class ListNode:
    def __init__(self, element_nodes, position_start, position_end):
        self.element_nodes = element_nodes
        self.position_start = position_start
        self.position_end = position_end

        # Make sure to pass positions in constructors for all nodes
