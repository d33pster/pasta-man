#
# This File contains the Exceptions related to PASTA-MAN only.
#

RESTRICTEDACTIVITY = "This activity is not permitted ->"

class InvalidKeyword(Exception):
    pass

class InvalidExportType(Exception):
    pass

class NoneTypeVariable(Exception):
    pass

class OptError(Exception):
    pass

class RestrictedActivity(Exception):
    pass