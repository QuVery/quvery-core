import bpy
RULE_NAME = "CreateCubeRule"


def process(input):
    bpy.ops.mesh.primitive_cube_add()
    print("CreateCubeRule: Cube has been created." + input)
    return True
