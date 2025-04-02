# Import necessary modules
import time
import bpy
import PIL
import numpy as np
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware  # Added import
import uvicorn
from rule_parser import (
    create_rules,
    get_rule_types,
    get_rules,
    execute_rules_for_file,
    execute_rules_in_directory,
    get_input_category,
)
from utils.logger import logger
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="QuVery Core API",
    description="The QuVery Core API is a REST API that allows you to check files against rules.",
    version="0.1.0",
    contact=dict(
        name="Omid Saadat",
        url="https://www.omid-saadat.com",
        email="info@omid-saadat.com",
    ),
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/live", tags=["Information"])
def check_the_server_live_status():
    """
    Root endpoint.
    """
    return {"message": "live"}


# @app.get("/rule_types")
# def get_rule_types_api():
#     """
#     Get a list of all available rule types.
#     """
#     return get_rule_types()


@app.get("/get_category/{input_path:path}", tags=["Information"])
def get_the_category_of_given_input(input_path: str = Path(...)):
    """
    Get the category of the given input.
    """
    logger.info(f"Getting category for input {input_path}")
    return get_input_category(input_path).value.lower()


@app.get("/rules", tags=["Information"])
async def get_all_available_rules_with_types(rule_type: Optional[str] = None):
    """
    Get a list of all available rules of the given type. use the rule type from the rule_types endpoint.
    """
    return get_rules(rule_type)


@app.get("/check/file/{file_path:path}", tags=["Check"])
async def check_file(file_path: str = Path(...)):
    """
    Check the given file against all rules of file type.
    """
    logger.info(f"Checking file {file_path}")
    result = execute_rules_for_file(file_path)
    return result


@app.get("/check/dir/{dir_path:path}", tags=["Check"])
async def check_dir(dir_path: str = Path(...), rule_type: Optional[str] = None):
    """
    Check the given directory against all rules for all files in the directory.
    """
    logger.info(f"Checking directory {dir_path}")
    st = time.time()
    result = execute_rules_in_directory(dir_path, rule_type)
    es = time.time()
    logger.info(f"Checked directory {dir_path} in {es-st} seconds")
    return result


def serve():
    """
    Serve the web application.
    """
    config = uvicorn.Config(app=app, port=8000, host="127.0.0.1", log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    logger.info("Starting QuVery Core API")
    create_rules()
    serve()
