import os

from AutoDoc.FileTypes.PythonFile import PythonFile

def document_directory(directory_path):
        """ Documents every python file in directory. """
        children = os.listdir(directory_path)
        python_files = list()
        
        for child in children: # Iterate over the children
            child = os.path.join(directory_path, child) # Extend the path
            
            if os.path.isdir(child): # If child is directory, add python files in that directory
                python_files = python_files + document_directory(child)
            elif child[-3:] == ".py": # Elif that child is a python file, add the file to the list
                python_files.append(child)
                    
        return python_files


def print_node_tree(node, indentation):
    ''' Prints out the tree structure and a string containing information about each node. '''
    text = node.type.tree_sign() + node.name + '\n\t- ' + node.doc_string

    # Print the text and add appropriate indentation for multiple line text
    for line in text.split('\n'):
        if line.strip() != '' and len(line.strip()) > 1:
            print('\t' * indentation + line)

    # Print the text for each child
    for child in node.children:
        print_node_tree(child, indentation + 1)



class AutoDoc:
    def __init__(self, directory_path):
        #TODO: Insert check
        self.directory_path = directory_path

    
    def scan(self):
        """ Scans and prints the contents of every python file in the directory. """
        for file in document_directory(self.directory_path):
            print_node_tree(PythonFile.create_tree(file), 0)

    