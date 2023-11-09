import bpy

RULE_NAME = "Load3DFile"
TYPE = "3D"

# https://docs.blender.org/api/current/bpy.ops.import_scene.html
# https://docs.blender.org/api/current/bpy.ops.wm.html


def process(input):
    blender_format = 'blend'
    default_3D_formats = ['fbx', 'obj', 'gltf', 'glb', 'x3d']
    wm_3D_formats = ['abc', 'dae', 'ply', 'stl', 'usd']
    # image_formats = ['jpg', 'jpeg', 'png', 'tga', 'tif', 'tiff', 'bmp', 'exr']
    # check the input file extension
    file_extension = input.split('.')[-1]

    if (file_extension in default_3D_formats or
        file_extension in wm_3D_formats or
            file_extension == blender_format):
        # file is a 3D model or a blender file
        # if the file is a blender file, we need to open it instead of importing it
        if (file_extension == blender_format):
            bpy.ops.wm.open_mainfile(filepath=input)
        else:
            # import the model file
            if (file_extension == 'glb'):
                file_extension = 'gltf'
            # replace the file extension with the import command
            if file_extension in default_3D_formats:
                bpy.ops.import_scene.__getattribute__(
                    file_extension)(filepath=input)
            elif file_extension in wm_3D_formats:
                bpy.ops.wm.__getattribute__(
                    file_extension + '_import')(filepath=input)
        return True
    # elif file_extension in image_formats:
    #     # file is an image
    #     # import the image file
    #     bpy.ops.image.open(filepath=input)
    #     return True
    else:
        # file is not a 3D model or an image
        print(
            f"LoadFile: file {input} is not supported as a 3D model.")
        return (RULE_NAME, f"File {input} is not supported as a 3D model.")
