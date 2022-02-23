#from msilib.schema import Directory
import os
#from tracemalloc import start

from AutoDoc.FileTypes.PythonFile import PythonFile
from AutoDoc.Node.Node import Node
from AutoDoc.Node.Types.Directory import FileDirectory
from AutoDoc.Node.Types.Class import Class
from AutoDoc.Node.Types.Method import Method
from AutoDoc.Node.Types.Variable import Variable
from AutoDoc.Node.Types.File import File
from AutoDoc.DocString import DocString

print_parameters =  {
    '-F': File,
    '-C': Class,
    '-M': Method,
    '-V': Variable,
    '-D': DocString,
}

print_scheme = {
    FileDirectory: True,
    File: True,
    Class: True,
    Method: True,
    Variable: True,
    DocString: True
}

def document_directory(directory_path):
    """ Documents every python file in directory. """
    directory_node = Node(FileDirectory, directory_path.split('/')[-1])
    children = os.listdir(directory_path)
    
    for child in children: # Iterate over the children
        child = os.path.join(directory_path, child) # Extend the path
        
        if os.path.isdir(child): # If child is directory, add python files in that directory
            child = document_directory(child)

            if child:
                directory_node.add_child(child)
        elif child[-3:] == ".py": # Elif that child is a python file, add the file to the list
            child = PythonFile.create_tree(child)
            directory_node.add_child(child)

    # Only add directory to structure if it contains a python file
    for child in directory_node.children:
        if child.type == File:
            return directory_node
                
    return None


def print_node_tree(node, indentation=0):
    ''' Prints out the tree structure and a string containing information about each node. '''

    if print_scheme[node.type] is False:
        return

    text = node.type.terminal_color + node.type.tree_sign() + node.name  + '\033[0m' # Print in specific colour and add endcode

    if node.doc_string:
        if print_scheme[DocString]:
            text += '\n\t-\033[94m ' + node.doc_string + '\033[0m'

    # Print the text and add appropriate indentation for multiple line text
    for line in text.split('\n'):
        if line.strip() != '' and len(line.strip()) > 1:
            print('\t' * indentation + line)

    # Print the text for each child
    for child in node.children:
        print_node_tree(child, indentation + 1)


def find_node_by_name(nodes, name):
    children = []

    for node in nodes:
        if node.name == name or (node.type == Method and node.name.split('(')[0] == name):
            return node
        else:
            children += node.children

    if len(children) == 0:
        print("No object was found by that name.") # Should be an error
        return None

    return find_node_by_name(children, name)


class AutoDoc:
    """ Scans and prints the contents of every python file in the directory. """
    def __init__(self, sys_arguments):
        self.directory_path = sys_arguments[1]

        # Only print from this subdirectory
        if len(sys_arguments) == 2 or (sys_arguments[2][0] == '-' and len(sys_arguments[2]) == 2):
            start_node = document_directory(self.directory_path)
        else:
            start_node = find_node_by_name([document_directory(self.directory_path)], sys_arguments[2])
            del sys_arguments[2]

        for parameter in sys_arguments[2:]:
            print_scheme[print_parameters[parameter]] = False

        print_node_tree(start_node)
    