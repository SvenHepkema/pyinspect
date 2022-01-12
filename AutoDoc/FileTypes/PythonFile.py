import re

from AutoDoc.Node.Node import Node 
from AutoDoc.Node.Types.Class import Class
from AutoDoc.Node.Types.File import File
from AutoDoc.Node.Types.Method import Method

def read_file(file_path):
    """ Reads a file into a list of lines. """
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    return lines

def convert_to_node(line):
    """ Converts a python code line into a node. Returns none if there is no appropiate node type found. """
    node_types = {
        "class": Class(),
        "def": Method()
    }

    keyword = line.lstrip().split(' ')[0].lower() # Extract the declaration statement from the line

    # Skip if it is not a declaration statement
    if keyword in node_types:
        return Node(node_types[keyword])
    else:
        return None

    
class PythonFile():
    def create_tree(pythonfile_path): #TODO: Save the name of the class/method to the node
        """ Converts a python file into a tree of nodes that represent the classes and methods in that file. """
        lines = read_file(pythonfile_path)

        start_node = Node(File)
        last_node = start_node
        last_count = -1 # -1 So functions and classes with zero indentation are childs of File

        for line in lines:
            new_node = convert_to_node(line)

            if new_node is None:
                continue
            
            # Add the new tree to the node tree 
            tab_count = re.search(r'[^\t]', line).start()
            if tab_count == last_count:
                last_node.add_sibling(new_node)
            elif tab_count > last_count:
                last_node.add_child(new_node)
            else:
                parent = last_node.return_parent(last_count - tab_count)
                parent.add_sibling(new_node)

            # Save the data for analysis of next node
            last_count = tab_count
            last_node = new_node

        return start_node



