# imports here
import bpy

# necessary for the rule to be loaded
RULE_NAME = "GetInfo3D"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "info"}  # default status is info
    details_json = {}

    # Implement your rule here and fill the details_json with the appropriate information or errors or leave it empty if there are no errors or warnings
    all_objects = bpy.data.objects
    details_json["OBJECTS"] = len(all_objects)
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    total_triangles = 0
    total_vertices = 0
    total_faces = 0
    for obj in mesh_objects:
        mesh = obj.data
        total_triangles += len(mesh.polygons)
        total_vertices += len(mesh.vertices)
        total_faces += len(mesh.polygons)
    details_json["TRIANGLES"] = total_triangles
    details_json["VERTICES"] = total_vertices
    details_json["FACES"] = total_faces

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
