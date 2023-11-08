import sys
import bpy
import os
import socket
from utils import ArgumentParser
from utils.logger import logger

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

# Function to execute all rules from the rules directory


def execute_rules():
    if getattr(sys, 'frozen', False):
        # We're running in a bundle
        base_path = os.path.dirname(sys.executable)
    else:
        # We're running in a normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    rules_path = os.path.join(base_path, 'rules')
    if not os.path.exists(rules_path):
        print(f"Rules directory not found: {rules_path}")
        return

    # Get a sorted list of rule files
    rule_files = sorted(
        [f for f in os.listdir(rules_path) if f.endswith('.py')])
    for rule_file in rule_files:
        rule_file_path = os.path.join(rules_path, rule_file)
        print(f"Executing rule: {rule_file}")
        execute_file(rule_file_path)


# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

# Start the server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server is listening on {host}:{port}...")
    execute_rules()
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
