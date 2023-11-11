# Import necessary modules
import bpy
import numpy as np
from fastapi import FastAPI, Path
import uvicorn
from rule_parser import create_rules, get_rule_types, get_rules, execute_rules_for_file, execute_rules_in_directory
from utils.logger import logger

create_rules()

# Initialize FastAPI app
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


@app.get("/rule_types")
def get_rule_types_api():
    """
    Get a list of all available rule types.
    """
    return get_rule_types()


@app.get("/rules/{rule_type}")
def get_rules_api(rule_type: str):
    """
    Get a list of all available rules of the given type. use the rule type from the rule_types endpoint.
    """
    return get_rules(rule_type)


@app.get("/check/file/{file_path:path}")
async def check_file(file_path: str = Path(...)):
    """
    Check the given file against all rules of file type.
    """
    logger.info(f"Checking file {file_path}")
    result = execute_rules_for_file(file_path)
    return result


@app.get("/check/dir/{dir_path:path}")
async def check_dir(dir_path: str = Path(...)):
    """
    Check the given directory against all rules for all files in the directory.
    """
    logger.info(f"Checking directory {dir_path}")
    result = execute_rules_in_directory(dir_path)
    return result


def serve():
    """
    Serve the web application.
    """
    config = uvicorn.Config(
        app=app, port=8000, host="127.0.0.1", log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    serve()
