
import socket


def send_code_to_server(ip, port, code):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(code.encode())
        print("Code has been sent to the server.")


# Configuration variables
server_ip = '127.0.0.1'  # Server IP address
server_port = 65432      # Server port

# Python code to send
python_code = """
import bpy
# create a cube
bpy.ops.mesh.primitive_cube_add()
"""

# Send the code to the server
send_code_to_server(server_ip, server_port, python_code)
