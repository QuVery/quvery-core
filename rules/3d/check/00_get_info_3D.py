import bpy

RULE_NAME = "GetInfo3D"

# this rule will return all information about the file:
# total Objects count in the file
# total triangle count
# total vertex count
# total face count


def process(input):
    report_json = {}
    all_objects = bpy.data.objects
    report_json["OBJECTS"] = len(all_objects)
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    total_triangles = 0
    total_vertices = 0
    total_faces = 0
    for obj in mesh_objects:
        mesh = obj.data
        total_triangles += len(mesh.polygons)
        total_vertices += len(mesh.vertices)
        total_faces += len(mesh.polygons)
    report_json["TRIANGLES"] = total_triangles
    report_json["VERTICES"] = total_vertices
    report_json["FACES"] = total_faces
    return report_json
