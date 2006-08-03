import sys

def SetItemError(theClass, name, value):
    ErrorString = "Exception! '%s' is not a valid value for '%s' attribute in '%s'.  Item not set.\n"
    sys.stderr.write(ErrorString % (value, name, theClass))

def AttrError(theClass, name):
    Attribute_Exception = "TRYING TO SET NONEXISTENT ATTRIBUTE '%s' in '%s'" % (name, theClass)
    raise Attribute_Exception

def MalformedPage(line):
    line = ' '.join(line)
    MalformedPage_Exception = "SYNTAX ERROR.  POTENTIALLY READING A MALFORMED GRACE FILE. LINE: '%s' CANNOT BE READ." % line
    #raise MalformedPage_Exception
    sys.stderr.write(MalformedPage_Exception+"\n")
    pass 
