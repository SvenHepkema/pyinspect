class Node:
    def __init__(self, type):
        self.parent = None
        self.type = type # Class/Function
        self.children = []

    
    def add_child(self, node):
        """ Adds a child node. """
        node.parent = self
        self.children.append(node)

    def add_sibling(self, node):
        """ Adds a child to the parent node. """
        self.parent.add_child(node)

    def return_parent(self, level):
        """ Goes up n levels (specified in the parameter) and returns the parent node. """
        parent = self.parent

        for i in range(level - 1): # Cycle up to the desired level
            if parent.parent is None:
                return parent
            else:
                parent = parent.parent

        return parent

    def __str__(self):
        result = self.type.__str__()

        for child in self.children:
            result += child.type.__str__()

        return result