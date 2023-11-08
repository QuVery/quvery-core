import sys
import bpy
from utils import ArgumentParser
from utils.logger import logger


import socket

bpy.ops.wm.read_factory_settings(use_empty=True)
logger.info("Resetting the internal state of Blender")

# Function to execute Python code from a string


def execute_code(code):
    try:
        # Allow bpy and built-ins to be available to the executed code
        exec_globals = {"__builtins__": __builtins__, "bpy": bpy}
        exec(code, exec_globals)
        print("Code has been executed.")
    except Exception as e:
        print(f"Error executing code: {e}")


# Function to execute Python code from a file


def execute_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            execute_code(code)
    except Exception as e:
        print(f"Error executing file: {e}")


# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

# Start the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server is listening on {host}:{port}...")

    # Server loop
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Convert bytes to string
                command = data.decode('utf-8')
                if command == 'exit':
                    print("Exit command received. Shutting down server.")
                    exit()
                elif command.endswith('.py'):
                    # Assume it's a filepath
                    execute_file(command)
                else:
                    # Assume it's a Python code string
                    execute_code(command)
