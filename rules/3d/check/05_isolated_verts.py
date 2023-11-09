import bpy

RULE_NAME = "IsolatedVerts"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        mesh = obj.data
        vert_edge_count = [0] * len(mesh.vertices)

        for edge in mesh.edges:
            vert_edge_count[edge.vertices[0]] += 1
            vert_edge_count[edge.vertices[1]] += 1

        for i, count in enumerate(vert_edge_count):
            if count == 0:
                errors_json[obj.name] = f"Isolated vertices (Vertex Index: {i})"

    if errors_json != {}:
        return errors_json
    else:
        return True
