import importlib
import os
import socket
import sys
from utils.logger import logger
import importlib.util

# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

precheck_rule_files = []
check_rule_files = []
postcheck_rule_files = []

precheck_modules = []
check_modules = []
postcheck_modules = []


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
                    data = conn.recv(1024)
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
    elif command.startswith('check '):
        file_name = command[6:]
        # we are dealing with a file as input
        result = check_input(file_name)
        conn.sendall(str(result).encode())


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


def check_input(input):
    # Now lets read all rules in the rules directory and execute them. rules are separate python files line r01_ruleone.py, r02_ruletwo.py, etc. we need to sort them by name to ensure they are executed in the correct order.
    rules_path = get_rules_path()
    precheck_subdir = os.path.join(rules_path, "1_precheck")
    check_subdir = os.path.join(rules_path, "2_check")
    postcheck_subdir = os.path.join(rules_path, "3_postcheck")

    precheck_rules = get_rule_files(precheck_subdir)
    check_rules = get_rule_files(check_subdir)
    postcheck_rules = get_rule_files(postcheck_subdir)

    precheck_result = process_rules(precheck_rules, precheck_subdir, input)
    check_result = process_rules(check_rules, check_subdir, input)
    postcheck_result = process_rules(postcheck_rules, postcheck_subdir, input)

    all_results = []
    all_results.extend(precheck_result)
    all_results.extend(check_result)
    all_results.extend(postcheck_result)

    return all_results


def process_rules(rules, subdir, input):
    error_result = []
    for rule in rules:
        # get the file name without the extension. rule contains the full path to the file with the extension
        rule_name = os.path.splitext(rule)[0]
        # Create a module spec
        spec = importlib.util.spec_from_file_location(
            rule_name, os.path.join(subdir, rule))
        # Create a module from the spec
        module = importlib.util.module_from_spec(spec)
        # Execute the module
        spec.loader.exec_module(module)
        # Execute the process function
        result = module.process(input)
        logger.info("Executing rule: " + rule + " - result: " + str(result))
        if (result != True):
            logger.error("Rule failed: " + rule)
            error_result.append(result)
    return error_result
