import bpy

RULE_NAME = "OverlapVerts"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        mesh = obj.data
        vert_coords = [vert.co for vert in mesh.vertices]

        # use a set to faster lookup
        unique_coords = set()
        for i, coord in enumerate(vert_coords):
            coord_tuple = tuple(coord)
            if coord_tuple in unique_coords:
                errors_json[obj.name] = f"Overlap vertices (Vertex Index: {i})"
            else:
                unique_coords.add(coord_tuple)
    if errors_json != {}:
        return errors_json
    else:
        return True
