import socket
import ssl
import sys
from cryptography.fernet import Fernet
import rsa

class Server:
    if __name__ == "__main__": 
        if(len(sys.argv) < 2):
            raise Exception("Usage: python bank_server.py <server_port>")
        port_number = sys.argv[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('new.pem', 'private.key')
        
        public_key, private_key = rsa.newkeys(1024)
        with open("server_public_Key.pem", "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))
       
        with open("server_private_Key.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))
    
        with open("server_public_Key.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
    
        with open("server_private_Key.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        
        sock.bind((socket.gethostname(), int(port_number)))
        print("Bank Server is listening on port {}".format(sys.argv[1]))
        while True:
            sock.listen(100)
            conn, address = sock.accept() 
            print("Connection from: " + str(address))
            encrypted_K = conn.recv(1024)
            key = rsa.decrypt(encrypted_K, private_key)
            with open("sym_key.key", "wb") as key_file:
                key_file.write(key)
           
            fernet_obj = Fernet(key)
            success = False
            while not success:  
                encrypted_creds = conn.recv(1024)
                decrypted_creds = fernet_obj.decrypt(encrypted_creds)
                username, entered_password = decrypted_creds.decode().split(" ")
                creds = username + " " + entered_password
                with open('password.txt', 'r') as f:
                    for line in f:
                        line = line.rstrip("\n").strip()
                        if creds == line:
                            success = True
                            conn.send("1".encode())
                            break
                if not success:
                    conn.send("0".encode())

            if success:
                while True:
                    choice = conn.recv(1).decode()
                    if choice == "1":
                        account_option = conn.recv(1024).decode()
                        if account_option not in ["1", "2"]:
                            conn.send("incorrect input".encode())
                        else:
                            transfer_data = conn.recv(1024).decode()
                            receiver_info = transfer_data.split("|")

                            if len(receiver_info) != 2:
                                conn.send("incorrect input".encode())
                                continue

                            receiver = receiver_info[0]
                            amount = receiver_info[1]
                            #print(f"Received transfer data: Receiver: {receiver}, Amount: {amount}")

                            # Recipient Check
                            recipient_exists = False
                            with open('balance.txt', 'r') as f:
                                for line in f:
                                    if line.strip().startswith(receiver):
                                        recipient_exists = True
                                        break

                            if not recipient_exists:
                                conn.send("recipient_not_exist".encode())
                            elif username == receiver:
                                conn.send("sender_and_recipient_are_same".encode())    
                            else:
                                # Proceed with the transaction logic only if the recipient exists
                                with open('balance.txt', 'r') as f:
                                    lines = f.readlines()

                                    for index, line in enumerate(lines):
                                        if line.startswith(receiver):
                                            _, recipient_savings_balance, recipient_checking_balance = line.split()

                                            recipient_balance = int(recipient_savings_balance) if account_option == "1" else int(recipient_checking_balance)

                                            # Check if the sender and recipient have the same type of accounts
                                            if (account_option == "1" and recipient_savings_balance) or (account_option == "2" and recipient_checking_balance):
                                               
                                                sufficient_funds = False
                                                with open('balance.txt', 'r') as f:
                                                    sender_lines = f.readlines()

                                                for sender_index, sender_line in enumerate(sender_lines):
                                                    if sender_line.startswith(username):
                                                        _, savings_balance, checking_balance = sender_line.split()
                                                        current_balance = int(savings_balance) if account_option == "1" else int(checking_balance)

                                                        if current_balance >= int(amount):
                                                           
                                                            sufficient_funds = True
                                                            break

                                                if not sufficient_funds:
                                                    conn.send("insufficient_funds".encode())
                                                    break

                                               
                                                if account_option == "1":
                                                    lines[index] = f"{receiver} {recipient_balance + int(amount)} {recipient_checking_balance}\n"
                                                else:
                                                    lines[index] = f"{receiver} {recipient_savings_balance} {recipient_balance + int(amount)}\n"

                                                #print("Updated Balance", lines[index])
                                                # Write the updated balances back to the file
                                                with open('balance.txt', 'w') as file:
                                                    file.writelines(lines)

                                              
                                                with open('balance.txt', 'r') as f:
                                                    sender_lines = f.readlines()

                                                for sender_index, sender_line in enumerate(sender_lines):
                                                    if sender_line.startswith(username):
                                                        _, savings_balance, checking_balance = sender_line.split()
                                                        current_balance = int(savings_balance) if account_option == "1" else int(checking_balance)

                                                        if account_option == "1":
                                                            sender_lines[sender_index] = f"{username} {current_balance - int(amount)} {checking_balance}\n"
                                                        else:
                                                            sender_lines[sender_index] = f"{username} {savings_balance} {current_balance - int(amount)}\n"

                                                        # Write the updated balances back to the file
                                                        with open('balance.txt', 'w') as file:
                                                            file.writelines(sender_lines)

                                                        conn.send("1".encode())  
                                                        break
                                                break
                                            else:
                                                conn.send("account_type_mismatch".encode())
                                                break
                    elif choice == "2":
                        with open('balance.txt', 'r') as f:
                            for line in f:
                                if line.startswith(username):
                                    _, savings_balance, checking_balance = line.split()
                                    balances_response = f"Your savings account balance: {savings_balance}\nYour checking account balance: {checking_balance}"
                                    conn.send(balances_response.encode())
                                    break
                    elif choice == "3":
                        conn.close()
                        break            