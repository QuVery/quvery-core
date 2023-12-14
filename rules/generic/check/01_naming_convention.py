import os
import re

# imports here

# necessary for the rule to be loaded


RULE_NAME = "NamingConvention"

def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    the function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    example: 
    for a single error: {"status": "error" , "details": {"object_name": "error message"}}
    for multiple errors: {"status": "error" , "details": {"object_name": "error message", "object_name2": "error message2"}}
    for a single warning: {"status": "warning" , "details": {"object_name": "warning message"}}
    for info: {"status": "info" , "details": {"object_name": "info message"}}
    """

    result_json = {"status": "error"} # default status is info
    details_json = {}

    # the naming convention for files is: [AssetTypePrefix]_[AssetName]_[Descriptor]_[OptionalVariantLetterOrNumber]
    # AssetTypePrefix is mandatory and can be like T for texture, SM for static mesh, A for audio clip, etc.
    # AssetName is mandatory and can be like: Tree, Rock, etc.
    # Descriptor is optional. like _Blue or _Zombie
    # OptionalVariantLetterOrNumber is optional. like _a or _1 or _a1

    match_regex = r"^[A-Z]{1,2}_[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*(_[a-zA-Z0-9]+)*(_[a-zA-Z0-9]+)*$"
    file_name_without_extension = os.path.splitext(os.path.basename(input))[0]
    if not re.match(match_regex, file_name_without_extension):
        details_json[file_name_without_extension] = f"File name '{file_name_without_extension}' does not match the naming convention: [AssetTypePrefix]_[AssetName]_[Descriptor]_[OptionalVariantLetterOrNumber]"
    
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
