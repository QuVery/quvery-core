import bpy

RULE_NAME = "GetInfo"

# this rule will return all information about the file:
# total Objects count in the file
# total triangle count
# total vertex count
# total face count


def process(input):
    report = ""
    all_objects = bpy.data.objects
    report += f"OBJECTS={len(all_objects)},"
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    total_triangles = 0
    total_vertices = 0
    total_faces = 0
    for obj in mesh_objects:
        mesh = obj.data
        total_triangles += len(mesh.polygons)
        total_vertices += len(mesh.vertices)
        total_faces += len(mesh.polygons)
    report += f"TRIANGLES={total_triangles},"
    report += f"VERTICES={total_vertices},"
    report += f"FACES={total_faces}"
    return report
