import bpy

RULE_NAME = "EdgeWithNoFace"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        mesh = obj.data
        edge_face_count = [0] * len(mesh.edges)

        for poly in mesh.polygons:
            for edge_key in poly.edge_keys:
                edge_idx = mesh.edge_keys.index(edge_key)
                edge_face_count[edge_idx] += 1

        for i, count in enumerate(edge_face_count):
            if count == 0:
                errors_json[obj.name] = f"Has edge with no face (Edge Index: {i})"
    if errors_json != {}:
        return errors_json
    else:
        return True
