from collections import Counter
import bpy

RULE_NAME = "EdgeWithNoFace"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}

    for obj in mesh_objects:
        mesh = obj.data
        edge_indices = {key: index for index, key in enumerate(mesh.edge_keys)}
        edge_face_count = Counter()

        for poly in mesh.polygons:
            for edge_key in poly.edge_keys:
                edge_idx = edge_indices[edge_key]
                edge_face_count[edge_idx] += 1

        errors = [
            f"Has edge with no face (Edge Index: {i})" for i, count in edge_face_count.items() if count == 0]
        if errors:
            errors_json[obj.name] = errors

    return errors_json if errors_json else True
