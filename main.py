import bpy
from server import start_server
from utils.logger import logger

bpy.ops.wm.read_factory_settings(use_empty=True)
logger.info("Resetting the internal state of Blender")

start_server()
