import bpy

RULE_NAME = "NoMaterialOnMesh"


def process(input):
    """
    This function is called for each file that is checked. The input is the file path.
    The function should return an empty json if the file is valid and a json object with the status and required information.
    status can be one of the following: "error", "warning", "info"
    """
    result_json = {"status": "error"}  # default status is error
    result_json["link"] = "https://github.com/QuVery/GameDevTechStandards/blob/main/Book/3D/ModelingTips.md#meshes-with-no-material"
    details_json = {}
    all_objects = bpy.data.objects
    mesh_objects = [obj for obj in all_objects if obj.type == "MESH"]
    for obj in mesh_objects:
        if not len(obj.material_slots):
            details_json[obj.name] = f"Has no material"
        # if the name of the material contains "default" or "Default" or "DEFAULT" then it is a default material and it is not allowed
        for material_slot in obj.material_slots:
            if "default" in material_slot.name.lower():
                details_json[obj.name] = f"Has a default material"
    if details_json != {}:
        result_json["details"] = details_json
        return result_json
    else:
        return {}
