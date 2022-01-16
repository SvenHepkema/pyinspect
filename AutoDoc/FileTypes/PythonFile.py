from ast import get_docstring
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

    words = line.lstrip().split(' ') # Extract the declaration statement from the line
    keyword = words[0].lower()
    statement = ' '.join(words[1:]).split(':')[0]

    # Skip if it is not a declaration statement
    if keyword in node_types:
        return Node(node_types[keyword], statement)
    else:
        return None

class DocString():
    def format():
        ''' Formats the docstring. '''
        # restructured text formatting?
        # * --> \n-
        # n* --> \n1-, \n2-
        # Remove all \n and replace all spaces with a single space
        # text = ' '.join(list(filter(None, text.replace('\n', ' ').split(' '))))


def get_docstrings(lines):
    """ Returns dictionary. Keys are line indexes of the class/method statements, value is the corresponding docstring."""
    text = ''.join(lines).replace("'''",'"""').split('"""') # Join lines to single text, normalize docstring notation, split by docstring delimiter #'''
    line_index = 0

    doc_strings = {} # Key: line index of start - 1 (So you get the corresponding object (class/method etc.)) Value: Doc string
    
    for index in range(len(text)):
        substring = text[index]

        # If it is a docstring
        if index % 2 == 1:
            doc_strings[line_index - 1] = substring

        # Keep track of the line index
        for character in substring:
            if character == '\n':
                line_index += 1

    return doc_strings

    
class PythonFile:
    def create_tree(pythonfile_path): #TODO: Save the name of the class/method to the node
        """ Converts a python file into a tree of nodes that represent the classes and methods in that file. """
        lines = read_file(pythonfile_path)

        start_node = Node(File, pythonfile_path.split('/')[-1])

        last_node = start_node
        last_count = -1 # -1 So functions and classes with zero indentation are childs of File

        doc_strings = get_docstrings(lines)

        for line_index in range(len(lines)):
            line = lines[line_index]
            new_node = convert_to_node(line)

            if new_node is None:
                continue
            
            # Add docstring
            if line_index in doc_strings:
                new_node.add_doc_string(doc_strings[line_index])

            # Calculate tab indentation level            
            line = line.replace('    ', '\t') # Convert 4 spaces to 1 tab
            tab_count = re.search(r'[^\t]', line).start()

            # Add the new tree to the node tree 
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



