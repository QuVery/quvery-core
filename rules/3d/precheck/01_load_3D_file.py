import os
import bpy

RULE_NAME = "Load3DFile"

# https://docs.blender.org/api/current/bpy.ops.import_scene.html
# https://docs.blender.org/api/current/bpy.ops.wm.html


def process(input):
    result_json = {"status": "error"}  # default status is error
    details_json = {}
    # delete all objects from the scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False, confirm=False)

    blender_format = "blend"
    default_3D_formats = ["fbx", "gltf", "glb", "x3d"]  # Removed 'obj'
    wm_3D_formats = ["abc", "dae", "ply", "stl", "usd", "obj"]  # Added 'obj'

    input = os.path.normpath(input)
    # check the input file extension
    file_extension = input.split(".")[-1].lower()

    if (
        file_extension in default_3D_formats
        or file_extension in wm_3D_formats
        or file_extension == blender_format
    ):
        # file is a 3D model or a blender file
        # if the file is a blender file, we need to open it instead of importing it
        if file_extension == blender_format:
            try:
                # print("Loading blender file: " + input)
                bpy.ops.wm.open_mainfile(filepath=input)
            except Exception as e:
                import traceback

                traceback.print_exc()
                print(f"An error occurred: {e.__class__.__name__}, {e}")
                details_json["error"] = (
                    f"An error occurred: {e.__class__.__name__}, {e}"
                )
                result_json["details"] = details_json
                return result_json
        else:
            # print("Loading 3D file: " + input)
            # import the model file
            try:
                if file_extension == "glb":
                    file_extension = "gltf"
                if file_extension == "dae":
                    file_extension = "collada"
                # replace the file extension with the import command
                if file_extension in default_3D_formats:
                    bpy.ops.import_scene.__getattribute__(file_extension)(
                        filepath=input
                    )
                elif file_extension in wm_3D_formats:
                    if file_extension == "obj":
                        bpy.ops.wm.obj_import(filepath=input)
                    else:
                        bpy.ops.wm.__getattribute__(file_extension + "_import")(
                            filepath=input
                        )
                return {}
            except Exception as e:
                import traceback

                traceback.print_exc()
                details_json["error"] = (
                    f"An error occurred: {e.__class__.__name__}, {e}"
                )
                result_json["details"] = details_json
                return result_json
    # elif file_extension in image_formats:
    #     # file is an image
    #     # import the image file
    #     bpy.ops.image.open(filepath=input)
    #     return True
    else:
        # file is not supported
        print(f"LoadFile: file {input} is not supported as a 3D model.")
        details_json["error"] = f"File {input} is not supported as a 3D model."
        result_json["details"] = details_json
        return result_json
