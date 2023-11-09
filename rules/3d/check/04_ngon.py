import bpy

RULE_NAME = "Ngons"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        mesh = obj.data
        for poly in mesh.polygons:
            if len(poly.vertices) > 4:
                errors_json[obj.name] = f"Has ngons - (Polygon Index: {poly.index})"
    if errors_json != {}:
        return errors_json
    else:
        return True
