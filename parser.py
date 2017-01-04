import re
import parserErrors
from xml import XML
from parserErrors import *


"""
Argument is a valid XML string without attributes. This string is parsed into
an XML object which is then returned. If input is falsey raises an
EmptyInputError. Invalid inputs will result in a TypeError.
"""
def parseXML(xmlString):
    if not xmlString:
        raise EmptyInputError
    # excludes xml/XML/Xml/etc, ensures it starts with letter or underscore
    validTag = r"(?![Xx][Mm][Ll])([A-Za-z_][A-Za-z0-9_\-.]*)"
    optionalHeader = r"(?:<\?xml[^<>?]*\?>)?"
    selfCloseString = r"^" + optionalHeader + r"<" + validTag + r" ?/>$"
    selfCloseRegex = re.compile(selfCloseString)
    selfClose = selfCloseRegex.search(xmlString)
    if selfClose:
        name = selfClose.group(1)
        tag = XML(name, [])
        return tag
    regexString = r"^" + optionalHeader + r"<" + validTag + r">(.*)</\1>$"
    regex = re.compile(regexString)
    result = regex.search(xmlString)
    if result is None:
        raise InvalidInputError(xmlString)
    name = result.group(1)
    contents = []
    inside = result.group(2)
    tagsRegex = re.compile(r"<" + validTag + r">(.*?)</\1>|<" + validTag + r" ?/>")
    innerTags = tagsRegex.finditer(inside)
    noMatch = True
    for innerTag in innerTags:
        noMatch = False
        inner = parseXML(innerTag.group())
        contents.append(inner)
    if inside and noMatch:
        raise InvalidInputError(inside)
    return XML(name, contents)
