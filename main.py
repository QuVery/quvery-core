# these imports are used here for pyinstaller to see and embed the python modules
import bpy  # https://pypi.org/project/bpy/
import numpy as np
from fastapi import FastAPI
import uvicorn
from rule_parser import create_rules, get_rule_types, get_rules
from utils.logger import logger

bpy.ops.wm.read_factory_settings(use_empty=True)
logger.info("Resetting the internal state of Blender")

create_rules()

app = FastAPI()

# get a list of all available rule types


@app.get("/rule_types")
def get_rule_types_api():
    return get_rule_types()

# get a list of all available rules of the given type


@app.get("/rules/{rule_type}")
def get_rules_api(rule_type: str):
    return get_rules(rule_type)


def serve():
    """Serve the web application."""
    uvicorn.run(app, port=8000)  # or whatever port number you want.


if __name__ == "__main__":
    serve()
