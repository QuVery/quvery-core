# these imports are used here for pyinstaller to see and embed the python modules
import bpy  # https://pypi.org/project/bpy/
import numpy as np
from fastapi import FastAPI, Path
import uvicorn
from rule_parser import create_rules, get_rule_types, get_rules, execute_rules_for_file, execute_rules_in_directory
from utils.logger import logger
from bpy.app.handlers import persistent


@persistent
def load_handler(dummy):
    print("Load Handler:", bpy.data.filepath)


bpy.app.handlers.load_post.append(load_handler)


create_rules()

app = FastAPI(
    title="QuVery Core API",
    description="The QuVery Core API is a REST API that allows you to check files against rules.",
    version="0.1.0",
    contact=dict(
        name="Omid Saadat",
        url="https://www.omid-saadat.com",
        email="info@omid-saadat.com",
    )
)

# get a list of all available rule types


@app.get("/rule_types")
def get_rule_types_api():
    return get_rule_types()

# get a list of all available rules of the given type


@app.get("/rules/{rule_type}")
def get_rules_api(rule_type: str):
    return get_rules(rule_type)

# check the given file against all rules of file type


@app.get("/check/{file_path:path}")
async def check_file(file_path: str = Path(...)):
    logger.info(f"Checking file {file_path}")
    result = execute_rules_for_file(file_path)
    return result

# check the given directory against all rules for all files in the directory


@app.get("/check_dir/{dir_path:path}")
async def check_dir(dir_path: str = Path(...)):
    logger.info(f"Checking directory {dir_path}")
    result = execute_rules_in_directory(dir_path)
    return result


def serve():
    """Serve the web application."""
    config = uvicorn.Config(
        app=app, port=8000, host="0.0.0.0", log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    serve()
