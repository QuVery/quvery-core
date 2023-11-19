# imports here
import math
import os
from PIL import Image
from utils.logger import logger

# necessary for the rule to be loaded
RULE_NAME = "GetInfo2D"


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
    result_json = {"status": "info"}  # default status is info
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings
    if not input.endswith(".exr"):
        im = Image.open(input)
        width, height = im.size
        details_json["WIDTH"] = width
        details_json["HEIGHT"] = height
    else:
        logger.info("EXR files are not supported yet.")
        details_json["ERROR"] = "EXR files are not supported yet."
    file_size = os.path.getsize(input)
    file_size = convert_size(file_size)
    details_json["SIZE"] = file_size

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}


def convert_size(size_bytes):
    """
    Convert the given file size in bytes to a human readable format.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
