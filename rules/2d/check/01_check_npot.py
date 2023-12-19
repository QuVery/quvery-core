# imports here
import os
import PIL.Image as Image
# necessary for the rule to be loaded
RULE_NAME = "Check NPOT"


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

    result_json = {"status": "error"}  # default status is info
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings
    # Check if the file dimensions are power of two
    # If not, return an error
    # If yes, return an empty json
    
    # Get the file extension
    _, ext = os.path.splitext(input)

    # Skip if the file is an EXR file
    if ext.lower() == '.exr':
        return {}
    
    img = Image.open(input)
    width, height = img.size
    if width & (width - 1) != 0 or height & (height - 1) != 0:
        details_json["NPOT"] = "Image dimensions are not power of two"

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
