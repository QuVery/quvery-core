from collections import Counter
import bpy

RULE_NAME = "EdgeWithNoFace"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "error"}  # default status is error
    result_json["link"] = "https://github.com/QuVery/GameDevTechStandards/blob/main/Book/3D/ModelingTips.md#edges-with-no-faces"
    details_json = {}
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]

    for obj in mesh_objects:
        mesh = obj.data
        edge_face_count = Counter({e.index: 0 for e in mesh.edges})

        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                edge_idx = mesh.loops[loop_index].edge_index
                edge_face_count[edge_idx] += 1

        errors = [
            f"Has edge with no face (Edge Index: {i})" for i, count in edge_face_count.items() if count == 0]
        if errors:
            details_json[obj.name] = errors

    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
