import bpy

RULE_NAME = "NoGeometryMesh"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "warning"}  # default status is info
    details_json = {}
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    for obj in mesh_objects:
        if not len(obj.data.vertices):
            details_json[obj.name] = f"Has no geometry"
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
