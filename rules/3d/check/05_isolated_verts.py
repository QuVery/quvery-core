import bpy

RULE_NAME = "IsolatedVerts"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "error"}  # default status is error
    details_json = {}
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]

    for obj in mesh_objects:
        mesh = obj.data
        vert_edge_count = [0] * len(mesh.vertices)

        for edge in mesh.edges:
            vert_edge_count[edge.vertices[0]] += 1
            vert_edge_count[edge.vertices[1]] += 1

        for i, count in enumerate(vert_edge_count):
            if count == 0:
                details_json[obj.name] = f"Isolated vertices (Vertex Index: {i})"

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
