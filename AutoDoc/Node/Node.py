from pydoc import doc


class Node:
    def __init__(self, type, name):
        self.parent = None
        self.type = type # Class/Function
        self.name = name
        self.children = []
        self.doc_string = ''

    
    def add_doc_string(self, doc_string):
        self.doc_string = doc_string
    
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