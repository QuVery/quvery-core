# these imports are used here for pyinstaller to see and embed the python modules
import bpy
import numpy as np

from server import start_server
from utils.logger import logger

bpy.ops.wm.read_factory_settings(use_empty=True)
logger.info("Resetting the internal state of Blender")

start_server()
