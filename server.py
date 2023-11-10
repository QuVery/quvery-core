import importlib
import json
import os
import socket
import sys
from types import ModuleType
from utils.logger import logger
import importlib.util
from rule_parser import create_rules, all_rules, get_input_type, get_rules_names
from rule_base import InputType
from error_codes import Error_Codes

# Configuration variables
host = '127.0.0.1'  # Localhost - ensures no remote access is allowed
port = 65432        # Port to listen on (non-privileged ports are > 1023)


def start_server():
    create_rules()
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
            send_message(conn, result)
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
            send_message(conn, help_text)
    elif command.startswith('check'):
        input = command[6:]
        # we are dealing with a file or path as input
        result = check_input(input)
        send_message(conn, result)
    else:
        send_message(conn, Error_Codes.UNKNOWN_COMMAND.value)


def send_message(conn: socket.socket, result):
    try:
        result = str(result)
        # Convert the result to bytes
        result_bytes = result.encode()
        total_length = len(result_bytes)
        # Prepare the header with fixed size, e.g., 10 bytes, representing the length
        header = f"{total_length:<10}".encode()
        # Send the header first
        conn.sendall(header)
        logger.info(f"Sent header with length: {total_length}")

        # Now send the actual data
        sent_length = 0
        for i in range(0, total_length, 1024):
            chunk = result_bytes[i:i+1024]
            conn.sendall(chunk)
            sent_length += len(chunk)
            logger.info(f"Sent {sent_length} of {total_length} bytes")
        logger.info(f"Result sent: {result}")
    except (BrokenPipeError, ConnectionResetError) as e:
        logger.error(f"Error occurred while sending data: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


def check_input(input):
    input_type = get_input_type(input)
    if input_type == InputType.UNSUPPORTED:
        return Error_Codes.FILE_NOT_VALID.value
    elif input_type == InputType.DIRECTORY:
        result: str = parse_directory(input)
        return result
    result = []
    for ruleList in all_rules:
        if ruleList.type == input_type:
            for module in ruleList.precheck_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                if process_result != True:
                    return f"Precheck failed at rule \"{module.RULE_NAME}\"."
            for module in ruleList.check_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                if process_result != True:
                    json_result = {}
                    json_result[module.RULE_NAME] = process_result
                    result.append(json_result)
            for module in ruleList.postcheck_rules:
                logger.info(f"Processing rule {module.RULE_NAME}")
                process_result = module.process(input)
                if process_result != True:
                    return f"Postcheck failed at rule \"{module.RULE_NAME}\"."
    return result


def parse_directory(input):
    # loop over all files and directories in the input directory
    # no matter if we are dealing with a file or a directory, when we call check_input we will get a list of results
    result_json = {}
    for entry in os.listdir(input):
        entry_path = os.path.join(input, entry)
        result = check_input(entry_path)
        result_json[entry_path] = result
    result_json = json.dumps(result_json)
    return result_json
