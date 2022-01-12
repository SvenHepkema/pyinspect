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

import AutoDoc

documentation = AutoDoc.AutoDoc(r"C:\Users\svenh\Documents\Example")

#documentation.select_directory()
documentation.scan_directory()
