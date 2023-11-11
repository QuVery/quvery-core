import math
import os
from PIL import Image
import OpenEXR

RULE_NAME = "GetInfo2D"

# this rule will return all information about the 2d file:
# File size
# Image dimensions


def process(input):
    report_json = {}
    # use PIL to get image dimensions if it is not an exr file
    if not input.endswith(".exr"):
        im = Image.open(input)
        width, height = im.size
        report_json["WIDTH"] = width
        report_json["HEIGHT"] = height
    else:
        # use OpenEXR to get image dimensions if it is an exr file
        exr = OpenEXR.InputFile(input)
        dw = exr.header()['dataWindow']
        width = dw.max.x - dw.min.x + 1
        height = dw.max.y - dw.min.y + 1
        report_json["WIDTH"] = width
        report_json["HEIGHT"] = height
    # get file size using os
    file_size = os.path.getsize(input)
    # convert file size to be pretty in KB, MB, GB, etc.
    file_size = convert_size(file_size)
    report_json["SIZE"] = file_size
    return report_json


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
