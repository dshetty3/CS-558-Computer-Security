import socket
import ssl
import sys
import getpass

class Client:
    if __name__ == "__main__":
        if len(sys.argv) < 3:
            raise Exception("Missing arguments: Has to be python3 cli.py <server_domain> <port_number>")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('/home/dshetty3/CS558-23f/p3-dshetty3/Server/cert.pem')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_host = sys.argv[1]
        remote_host_ip = socket.gethostbyname(remote_host)
        port_number = int(sys.argv[2])

        sock.connect((remote_host_ip, port_number))
        print("Connection established")

        while True:
            username = input("Enter your ID: ")
            password = getpass.getpass("Enter your password: ")

            credentials = f"{username} {password}"
            sock.send(credentials.encode())
            print(f"Sent: {credentials}")

            response = sock.recv(1024).decode()
            print(f"Received: {response}")

            if response == "Correct ID and password":
                break
