"""
Base class for parser errors
"""
class ParserError(Exception):
    pass

"""
Raised when the input to parser is an empty string, or other falsey value
"""
class EmptyInputError(ParserError):
    def __init__(self):
        self.message = "parser input was an empty string"

"""
Raised when the input to parser is not valid xml. Argument is the particular
string input that triggered the error.
"""
class InvalidInputError(ParserError):
    def __init__(self, inputString):
        self.input = inputString
        self.message = "Invalid xml: " + inputString
