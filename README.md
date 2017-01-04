## XML Parser
### By Deanna Heer for Oceanit

The parser itself is located in `parser.py`. The function `parseXML` takes in an
XML string and returns a parsed XML object. That string can be an entire XML
document (with the <?xml?> header, which is ignored) or just valid XML. The
parser will raise an exception if the string is invalid or empty.

#### Tests
There are tests for both the parser and the XML class in tests.py. These tests
can be run using the command `python tests.py` within this directory.
