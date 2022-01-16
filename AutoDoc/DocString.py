def format(string):
        ''' Formats the docstring. '''
        # reStructuredText formatting?

        # Remove all \n and replace all spaces with a single space
        string = ' '.join(list(filter(None, string.replace('\n', ' ').split(' '))))

        return string


class DocString:
    def __init__(self, string):
        self.string = format(string)
    
    def __str__(self):
        return self.string