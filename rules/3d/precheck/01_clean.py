import bpy

RULE_NAME = "Clean"

def process(input):
    """
    Deletes all default objects (camera, light and cube) from the scene.

    Args:
        input: Unused argument.

    Returns:
        True.
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    return True
