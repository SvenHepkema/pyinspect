import re

from pyinspect.Node.Node import Node 
from pyinspect.Node.Types.Class import Class
from pyinspect.Node.Types.File import File
from pyinspect.Node.Types.Method import Method
from pyinspect.Node.Types.Variable import Variable
from pyinspect.DocString import DocString


def read_file(file_path):
    """ Reads a file into a list of lines. """
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    return lines

def convert_to_node(parent, line):
    """ Converts a python code line into a node. Returns none if there is no appropiate node type found. """
    node_types = {
        "class": Class,
        "def": Method
    }

    words = line.lstrip().replace('.', ' ').split(' ') # Extract the declaration statement from the line
    keyword = words[0].lower()
    statement = ' '.join(words[1:]).split(':')[0]

    # Skip if it is not a declaration statement
    if keyword in node_types:
        return Node(node_types[keyword], statement)
    elif '=' in line and line.lstrip()[0] != '#' and len(line.split('=')[0].strip().split(' ')) == 1: # If it is a stand alone, static variable or variable in a init method
        if parent.type is Method and parent.name.split('(')[0].strip() == "__init__": # Vars in init methods
            return Node(Variable, line.split('=')[0].strip())
        elif parent.type is Class or parent.type is File: # Vars in class or files
            return Node(Variable, line.split('=')[0].strip())
    else:
        return None
    

def get_docstrings(lines):
    """ Returns dictionary. Keys are line indexes of the class/method statements, value is the corresponding docstring."""
    text = ''.join(lines).replace("'''",'"""').split('"""') # Join lines to single text, normalize docstring notation, split by docstring delimiter #'''
    line_index = 0

    doc_strings = {} # Key: line index of start - 1 (So you get the corresponding object (class/method etc.)) Value: Doc string
    
    for index in range(len(text)):
        substring = text[index]

        # If it is a docstring
        if index % 2 == 1:
            doc_strings[line_index - 1] = DocString(substring)

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
            # Calculate tab indentation level       
            line = lines[line_index]     
            line = line.replace('    ', '\t') # Convert 4 spaces to 1 tab
            
            if len(line.strip()) > 0:
                tab_count = re.search(r'[^\t]', line).start()
            
            # Get the parent and identify whether it is a child or sibling of the last analyzed node
            parent = last_node

            if tab_count == last_count:
                parent = last_node.parent
            elif tab_count < last_count:
                parent = last_node.return_parent(last_count - tab_count + 1)
            else:
                parent = last_node
            
            new_node = convert_to_node(parent, line)

            if new_node is None:
                continue
            
            # Add docstring
            if line_index in doc_strings:
                new_node.add_doc_string(doc_strings[line_index])

            # Add the new tree to the node tree 
            parent.add_child(new_node)

            # Save the data for analysis of next node
            last_count = tab_count
            last_node = new_node

        return start_node



