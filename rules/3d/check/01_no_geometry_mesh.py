import bpy

RULE_NAME = "NoGeometryMesh"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        if not len(obj.data.vertices):
            errors_json[obj.name] = f"Has no geometry"
    if errors_json != {}:
        return errors_json
    else:
        return True
