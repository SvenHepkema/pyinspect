import os

import tkinter
from tkinter import filedialog

from AutoDoc.FileTypes import PythonFile

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

class AutoDoc:
    def __init__(self, directory_path=None):
        self.directory_path = directory_path


    def select_directory(self):
        """ Uses Windows file explorer to select a folder to scan for and document any python code found. """
        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        self.directory_path = tkinter.filedialog.askdirectory()

    
    def scan_directory(self):
        """ Scans and prints the contents of every python file in the directory. """
        for file in document_directory(self.directory_path):
            print(PythonFile.PythonFile.create_tree(file))

    