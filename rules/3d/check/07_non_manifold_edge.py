import bpy

RULE_NAME = "NonManifoldEdge"


def process(input):
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    errors_json = {}
    for obj in mesh_objects:
        mesh = obj.data
        edge_face_count = [0] * len(mesh.edges)
        # Count the number of faces each edge is part of
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                edge_index = mesh.loops[loop_index].edge_index
                edge_face_count[edge_index] += 1

        # Check if any edge has more than 2 linked faces (non-manifold)
        for i, count in enumerate(edge_face_count):
            if count > 2:
                errors_json[obj.name] = f"Non-manifold edge (Edge Index: {i})"
    if errors_json != {}:
        return errors_json
    else:
        return True
