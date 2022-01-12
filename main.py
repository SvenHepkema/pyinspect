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


from AutoDoc import AutoDoc

documentation = AutoDoc.AutoDoc(r"C:\Users\svenh\Documents\Example")

#documentation.select_directory()
documentation.scan_directory()
