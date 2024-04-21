#
# Terminal Exceptions
#

class ArgumentError(Exception):
    ARGUMENTERROR = "Error:"
    pass

class EmptyArgument(Exception):
    EMPTYARGUMENT = "No Arguments passed!"
    pass