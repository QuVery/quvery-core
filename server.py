import importlib
import os
import socket
import sys
from utils.logger import logger
import importlib.util

# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)

# Function to execute Python code from a string


def execute_code(code):
    logger.info("Executing code from a string")

# Function to execute Python code from a file


def execute_file(file_path):
    logger.info("Executing with input file: {}".format(file_path))

# Function to execute all rules from the rules directory


def execute_rules():
    logger.info("Executing all rules")


def start_server():
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
                    if command == 'exit':
                        logger.info(
                            "Exit command received. Shutting down server.")
                        sys.exit()
                    else:
                        # dispatch an event to notify main.py that a command has been received
                        logger.info("Command received: {}".format(command))
                        result = check_input(command)
                        # result is an array of strings or boolean values. we need to convert it to a single string
                        result = str(result)
                        conn.sendall(result.encode())


def get_rules(rules_path):
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
    logger.info("Checking input: " + input)
    # Now lets read all rules in the rules directory and execute them. rules are separate python files line r01_ruleone.py, r02_ruletwo.py, etc. we need to sort them by name to ensure they are executed in the correct order.
    rules_path = get_rules_path()
    precheck_subdir = os.path.join(rules_path, "1_precheck")
    check_subdir = os.path.join(rules_path, "2_check")
    postcheck_subdir = os.path.join(rules_path, "3_postcheck")

    precheck_rules = get_rules(precheck_subdir)
    check_rules = get_rules(check_subdir)
    postcheck_rules = get_rules(postcheck_subdir)

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
        if (result == False):
            logger.error("Rule failed: " + rule)
            error_result.append(result)
    return error_result
