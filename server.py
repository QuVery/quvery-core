import socket
from utils.logger import logger
from check_input import check_input

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
                        exit()
                    else:
                        # dispatch an event to notify main.py that a command has been received
                        logger.info("Command received: {}".format(command))
                        result = check_input(command)
                        conn.sendall(result.encode())
