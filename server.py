import importlib
import os
import socket
import sys
from types import ModuleType
from utils.logger import logger
import importlib.util
from enum import Enum

# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

precheck_rule_files = []
check_rule_files = []
postcheck_rule_files = []

precheck_modules = []
check_modules = []
postcheck_modules = []


class InputType(Enum):
    DEFAULT = "DEFAULT"
    DIRECTORY = "DIR"
    FILE_3D = "3D"
    FILE_2D = "2D"


class Error_Codes(Enum):
    NO_ERROR = ""
    FILE_NOT_FOUND = "Error: File does not exist. Use a valid file path after \"check\" command"
    FILE_NOT_VALID = "Error: File is not valid."
    MODULE_HAS_NO_RULE_NAME = "Error: Module does not have a RULE_NAME attribute."
    UNKNOWN_COMMAND = "Error: Unknown command. Use \"help\" to get a list of all available commands."


def start_server():
    create_modules()
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


def create_modules():
    # Read all rules in the rules directory and subdirectories.
    # rules are separate python files
    rules_path = get_rules_path()
    precheck_subdir = os.path.join(rules_path, "1_precheck")
    check_subdir = os.path.join(rules_path, "2_check")
    postcheck_subdir = os.path.join(rules_path, "3_postcheck")

    precheck_rule_files = get_rule_files(precheck_subdir)
    check_rule_files = get_rule_files(check_subdir)
    postcheck_rule_files = get_rule_files(postcheck_subdir)

    for rule in precheck_rule_files:
        create_module_from_file(precheck_subdir, rule, precheck_modules)

    for rule in check_rule_files:
        create_module_from_file(check_subdir, rule, check_modules)

    for rule in postcheck_rule_files:
        create_module_from_file(postcheck_subdir, rule, postcheck_modules)


def create_module_from_file(subdir, rule, modules):
    # get the file name without the extension. rule contains the full path to the file with the extension
    rule_name = os.path.splitext(rule)[0]
    # Create a module spec
    spec = importlib.util.spec_from_file_location(
        rule_name, os.path.join(subdir, rule))
    # Create a module from the spec
    module = importlib.util.module_from_spec(spec)

    # Load the module; this is necessary to access module attributes
    spec.loader.exec_module(module)

    module_name = getattr(module, "RULE_NAME", None)
    if module_name is not None:
        modules.append(module)
        logger.info("Loaded module: " + module_name)
    else:
        logger.error(
            f"Module {rule_name} does not have a RULE_NAME attribute.")


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
            result = get_commands()
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
        input_type = get_input_type(input)
        logger.info(f"Input type: {input_type}")
        if input_type == InputType.FILE_3D:
            result = check_file(input)
            conn.sendall(str(result).encode())
        elif input_type == InputType.FILE_2D:
            result = check_file(input)
            conn.sendall(str(result).encode())
        elif input_type == InputType.DIRECTORY:
            result = process_directory(input)
            conn.sendall(str(result).encode())
        else:
            logger.error(Error_Codes.FILE_NOT_VALID.value)
            conn.sendall(Error_Codes.FILE_NOT_VALID.value.encode())
    else:
        logger.error(f"Unknown command {command}")
        conn.sendall(Error_Codes.UNKNOWN_COMMAND.value.encode())


def get_commands():
    # The command name is a variable called RULE_NAME in each module
    commands = []
    for module in precheck_modules:
        commands.append(getattr(module, "RULE_NAME", None))
    for module in check_modules:
        commands.append(getattr(module, "RULE_NAME", None))
    for module in postcheck_modules:
        commands.append(getattr(module, "RULE_NAME", None))
    logger.info("Available commands: " + str(commands))
    return commands


def get_rule_files(rules_path):
    rules = []
    for file in os.listdir(rules_path):
        if file.endswith(".py"):
            rules.append(file)
    rules.sort()
    return rules


def get_rules_path():
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        application_path = os.path.dirname(sys.executable)
    else:
        # we are running in a normal Python environment
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, "rules")


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


def check_file(input):
    input_type = get_input_type(input)
    # process precheck rules with adding the result to the result list
    for module in precheck_modules:
        if module_matches(module, input_type):
            logger.info(f"Processing rule {module.RULE_NAME}")
            process_result = module.process(input)
            if process_result != True:
                return "Precheck failed. File is not valid."

    result = []
    # Check rules
    for module in check_modules:
        if module_matches(module, input_type):
            logger.info(f"Processing rule {module.RULE_NAME}")
            rule_name = getattr(module, "RULE_NAME", None)
            if rule_name is not None:
                process_result = module.process(input)
                if process_result != True:
                    result_pair = {
                        rule_name,
                        process_result
                    }
                    result.append(result_pair)
            else:
                logger.error(Error_Codes.MODULE_HAS_NO_RULE_NAME.value)
                result.append(
                    Error_Codes.MODULE_HAS_NO_RULE_NAME.value + f"Skipping invalid rule {module}")
    # process postcheck rules with adding the result to the result list
    for module in postcheck_modules:
        if module_matches(module, input_type):
            logger.info(f"Processing rule {module.RULE_NAME}")
            process_result = module.process(input)
            if process_result != True:
                result_pair = {
                    rule_name,
                    process_result
                }
                result.append(result_pair)
        module.process(input)

    return result


def module_matches(module: ModuleType, module_type: InputType):
    # if module type is DEFAULT or it matches the input type, return true else return false
    if module.TYPE == module_type.value or module_type == InputType.DEFAULT.value:
        return True
    return False


def process_directory(input):
    # parse the directory and get all files with all formats
    return InputType.DIRECTORY.value
