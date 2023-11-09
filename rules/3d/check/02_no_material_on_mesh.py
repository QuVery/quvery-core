import bpy

RULE_NAME = "NoMaterialOnMesh"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        if not len(obj.material_slots):
            errors_json[obj.name] = f"Has no material"
    if errors_json != {}:
        return errors_json
    else:
        return True
