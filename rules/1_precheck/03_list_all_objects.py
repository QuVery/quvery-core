import bpy

RULE_NAME = "ListAllObjects"


def process(input):
    for obj in bpy.data.objects:
        print("ListAllObjectsRule: obj: " + input + " - " + obj.name)
    return True
