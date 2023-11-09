import bpy

RULE_NAME = "NoGeometryMesh"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors = ""
    for obj in mesh_objects:
        if not len(obj.data.vertices):
            errors += (f"File: {input} - The object \"{obj.name}\" is a mesh, but has no geometry")
    return errors
