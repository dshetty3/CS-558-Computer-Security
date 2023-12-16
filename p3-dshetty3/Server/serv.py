import socket
import ssl
import sys
import hashlib

# Load hashed passwords from the "hashpasswd" file
def load_passwords():
    passwords = {}
    with open('/home/dshetty3/CS558-23f/p3-dshetty3/hashpasswd', 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                user = parts[0]
                hashed_password = parts[1]
                passwords[user] = hashed_password
    return passwords


class Server:
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            raise Exception("Missing arguments: Has to be python3 serv.py <port_number>")

        port_number = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        sock.bind((socket.gethostname(), port_number))
        sock.listen(1)
        print(f"Server listening on port {port_number}")

        passwords = load_passwords()

        while True:
            try:
                connection, client_address = sock.accept()
                with connection:
                    print(f"Connected by {client_address}")
                    while True:
                        data = connection.recv(1024)
                        if not data:
                            break

                        data_str = data.decode()
                        #print(f"Received data: {data_str}")

                        username, password = data_str.split()
                        if username in passwords:
                            provided_hash = hashlib.sha256(password.encode()).hexdigest()
                            #print(f"Expected hash: {passwords[username]}, Provided hash: {provided_hash}")
                            if provided_hash == passwords[username]:
                                connection.send("Correct ID and password".encode())
                                #print("Sent: Correct ID and password")
                                break
                        connection.send("The ID/password is incorrect".encode())
                        #print("Sent: The ID/password is incorrect")

            except Exception as e:
                print(f"Error: {e}")
                break
            finally:
                connection.close()
