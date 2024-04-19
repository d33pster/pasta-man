"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
    - external:
        - description: Needs to be installed using pip.
    - Project Specific
        - description: Modules made for this project.
        - contents:

Hierarchy:
    - exceptions.py:
        - contents:
            InvalidKeyword
            InvalidExportType
            NoneTypeVariable
            - OptError (class):
                - contents:
                    OPTIONERROR (const)
            - RestrictedActivity (class):
                - contents:
                    RESTRICTEDACTIVITY (const)
InvalidKeyword:
    - description: Exception for Invalid Keyword.

InvalidExportType:
    - description: Exception for Invalid Export Type.

NoneTypeVariable:
    - description: Exception for None Type Variable.

OptError:
    - description: Exception for Option Error.
    
    - OPTIONERROR (const):
        - description: contains default prefix text for OptError
        - value: 'Option Error:'

RestrictedActivity:
    - description: Exception for Restricted Activity.

    - RESTRICTEDACTIVITY (const):
        - description: Contains default prefix text for RestrictedActivity Exception.
        - value: 'This activity is not permitted:'            

InvalidExportType:
    - description: Exception for Invalid File type of import
    
    - INVALIDIMPORTTYPE (const):
        - description: contains default prefix text for InvalidExportType Exception.
"""

# Invalid Keyword Exception
class InvalidKeyword(Exception):
    pass

# Invalid Export Type Exception
class InvalidExportType(Exception):
    pass

# None Type Variable Exception
class NoneTypeVariable(Exception):
    pass

# Option Error Exception
class OptError(Exception):
    OPTIONERROR = "Option Error:"
    pass

# Restricted Activity Exception
class RestrictedActivity(Exception):
    RESTRICTEDACTIVITY = "This activity is not permitted:" # exception constant
    pass

class InvalidImportType(Exception):
    INVALIDIMPORTTYPE = "This File format is not yet supported:"
    pass