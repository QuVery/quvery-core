import importlib
import os
import socket
import sys
from types import ModuleType
from utils.logger import logger
import importlib.util
import rule_parser
from rule_base import InputType
import error_codes as Error_Codes
from enum import Enum

# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

def start_server():
    rule_parser.create_rules()
    # Start the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logger.info(f"Server is listening on {host}:{port}...")
        # Server loop
        while True:
            conn, addr = s.accept()
            with conn:
                logger.info(f"Connected by {addr}")
                while True:
                    try:
                        data = conn.recv(1024)
                    except (BrokenPipeError, ConnectionResetError) as e:
                        logger.error(f"Error occurred: {e}")
                        break
                    if not data:
                        break
                    # Convert bytes to string
                    command = data.decode('utf-8')
                    parse_command(command, conn)

def parse_command(command, conn):
    command_list = [
        'exit',
        'get_rules',
        'help'
    ]
    if command in command_list:
        # we are dealing with an internal command
        if command == 'get_rules':
            # get a list of all available check rules
            result = get_rules_names()
            conn.sendall(str(result).encode())
        elif command == 'exit':
            logger.info(
                "Exit command received. Shutting down server.")
            sys.exit()
        elif command == 'help':
            help_text = "Available commands:\n"
            help_text += "check <file_path> - check the file with all rules\n"
            help_text += "get_rules         - get a list of all available check rules\n"
            help_text += "help              - get a list of all available commands\n"
            help_text += "exit              - exit the server\n"
            conn.sendall(help_text.encode())
    elif command.startswith('check'):
        input = command[6:]
        # we are dealing with a file or path as input
        result = check_input(input)
        logger.info(f"Returning result: {result}")
        conn.sendall(str(result).encode())
    else:
        logger.error(f"Unknown command {command}")
        conn.sendall(Error_Codes.UNKNOWN_COMMAND.value.encode())


def get_rules_names():
    # The command name is a variable called RULE_NAME in each module
    commands = []
    for ruleList in rule_parser.all_rules:
        for module in ruleList.check_rules:
            commands.append(module.RULE_NAME)
        for module in ruleList.precheck_rules:
            commands.append(module.RULE_NAME)
        for module in ruleList.postcheck_rules:
            commands.append(module.RULE_NAME)
    return commands

def get_input_type(input):
    file_extension = input.split('.')[-1]
    if os.path.isfile(input):
        if file_extension in ['fbx', 'obj', 'gltf', 'glb', 'x3d', 'abc', 'dae', 'ply', 'stl', 'usd', 'blend']:
            return InputType.FILE_3D
        elif file_extension in ['jpg', 'jpeg', 'png', 'tga', 'tif', 'tiff', 'bmp', 'exr', 'psd']:
            return InputType.FILE_2D
        else:
            return InputType.DEFAULT
    elif os.path.isdir(input):
        return InputType.DIRECTORY


def check_input(input):
    input_type = get_input_type(input)
    result = []
    for ruleList in rule_parser.all_rules:
        if ruleList.type == input_type:
            for module in ruleList.precheck_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                if process_result != True:
                    return f"Precheck failed at rule \"{module.RULE_NAME}\"."
            for module in ruleList.check_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                json_result = {}
                json_result[module.RULE_NAME] = process_result
                result.append(json_result)
            for module in ruleList.postcheck_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                if process_result != True:
                    return f"Postcheck failed at rule \"{module.RULE_NAME}\"."
    return result