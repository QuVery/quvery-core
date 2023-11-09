from enum import Enum

class Error_Codes(Enum):
    NO_ERROR = ""
    FILE_NOT_FOUND = "Error: File does not exist. Use a valid file path after \"check\" command"
    FILE_NOT_VALID = "Error: Invalid file."
    MODULE_HAS_NO_RULE_NAME = "Error: Module does not have a RULE_NAME attribute."
    UNKNOWN_COMMAND = "Error: Unknown command. Use \"help\" to get a list of all available commands."
