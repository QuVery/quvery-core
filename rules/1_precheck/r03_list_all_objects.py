import bpy
RULE_NAME = "ListAllObjectsRule"


def process(input):
    for obj in bpy.data.objects:
        print("ListAllObjectsRule: obj: " + input + " - " + obj.name)
    return True
