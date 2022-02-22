# Targets: own inspection module
# Give option to give hints in comments for compilation of comments in the documentation.
# Such as #[1] or #[*] for summation, or #[">] #[<"] to quote comment

# Another example:
# !RETURN NONE IF "No appropriate type is found" ELSE RETURN NODE!
# ==>
# Returns
# If no appropriate type is found:
#   - None 
# Else
#   - Node --> Hyperlink to python object declaration node in documentation.

# Compile pdf with the resulting documentation
# Customization in mind (Customizer delimiters and keywords that trigger the documentation, but also keep the setup open for expansion)
# - config file

# Config file structure:
# The syntax is completely customizable, the base syntax is a config itself.

# Interactive shell:
# Make it so that you can inspect python codebases in the terminal with autodoc, and maybe test functions live with test inputs

# Extend support for documenting different file types

# Make it more general so supporting different file type is easier

# Make general customization functions such as catch('delimiter', text) instead of get_docstrings(text)

# Make some format options such as * --> \n and remove useless '\n' in comments

# Make error mode: inspect all raises of possible errors

import sys

from AutoDoc.AutoDoc import AutoDoc

#TODO: Set up all the cli arguments. -- Make a module for handling it?

# TERMINAL-COMMAND: [1] target directory

documentation = AutoDoc(sys.argv[1])
documentation.scan()
