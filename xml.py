"""
A class to represent XML strings.
"""
class XML:
    """
    XML Constructor. name is the tag name. contents is a list of XML objects
    that are within this tag.
    """
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    """
    Compare this XML with another XML. Returns true if they are the same
    (meaning they have the same name and same tags in the same order and
    recursively checks all of the inner tags all the way down) or false
    otherwise.
    """
    def compare(self, other):
        if self.name != other.name:
            return False
        if len(self.contents) != len(other.contents):
            return False
        for i in range(len(self.contents)):
            selfTag = self.contents[i]
            otherTag = other.contents[i]
            if not selfTag.compare(otherTag):
                return False
        return True
