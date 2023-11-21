import bpy

RULE_NAME = "OverlapVerts"


def process(input):
    result_json = {"status": "warning"}  # default status is error
    result_json["link"] = "https://github.com/QuVery/GameDevTechStandards/blob/main/Book/3D/ModelingTips.md#overlapping-vertices"
    details_json = {}
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    for obj in mesh_objects:
        mesh = obj.data
        vert_coords = [vert.co for vert in mesh.vertices]

        # use a set to faster lookup
        unique_coords = set()
        for i, coord in enumerate(vert_coords):
            coord_tuple = tuple(coord)
            if coord_tuple in unique_coords:
                details_json[obj.name] = f"Overlap vertices (Vertex Index: {i})"
            else:
                unique_coords.add(coord_tuple)
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
