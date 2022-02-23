import os

from AutoDoc.FileTypes.PythonFile import PythonFile
from AutoDoc.Node.Node import Node
from AutoDoc.Node.Types.Directory import FileDirectory
from AutoDoc.Node.Types.File import File
from AutoDoc.DocString import DocString

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

    text = node.type.terminal_color + node.type.tree_sign() + node.name  + '\033[0m' # Print in specific colour and add endcode

    if node.doc_string:
        text += '\n\t-\033[94m ' + node.doc_string + '\033[0m'

    # Print the text and add appropriate indentation for multiple line text
    for line in text.split('\n'):
        if line.strip() != '' and len(line.strip()) > 1:
            print('\t' * indentation + line)

    # Print the text for each child
    for child in node.children:
        print_node_tree(child, indentation + 1)



class AutoDoc:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    
    def scan(self):
        """ Scans and prints the contents of every python file in the directory. """
        print_node_tree(document_directory(self.directory_path))
    