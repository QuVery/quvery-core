
# imports here
import math
import bpy

# necessary for the rule to be loaded
RULE_NAME = "Is Transform Applied"


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
    result_json["link"] = "https://github.com/QuVery/GameDevTechStandards/blob/main/Book/3D/ModelingTips.md#applied-transforms"
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            # Check if the scale and rotation are applied
            if not all(math.isclose(i, 1, abs_tol=1e-9) for i in obj.scale):
                details_json[obj.name] = "Scale is not applied"
            if not all(math.isclose(i, 0, abs_tol=1e-9) for i in obj.rotation_euler):
                details_json[obj.name] = "Rotation is not applied"

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
