import socket


def send_code_to_server(ip, port, code):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(code.encode())
        print("Code has been sent to the server.")

        # Listen for a response
        data = s.recv(1024)
        print('Received from server:', data.decode())


def main(server_ip, server_port):
    while True:
        # Get input from the user
        code = input("Enter your message (or 'exit' to quit): ")

        # Break the loop if the user types 'exit'
        if code.lower() == 'exit':
            print("Exiting the client.")
            break

        # Send the code to the server
        send_code_to_server(server_ip, server_port, code)


# Configuration variables
server_ip = '127.0.0.1'  # Server IP address
server_port = 65432      # Server port

if __name__ == "__main__":
    main(server_ip, server_port)
