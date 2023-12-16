import socket
import ssl
import sys
from cryptography.fernet import Fernet
import rsa
import getpass

class Client:
        
    if __name__ == "__main__": 
        if(len(sys.argv) < 2):
            raise Exception("Missing arguements")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('new.pem')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_host = sys.argv[1]
        remote_host_ip = socket.gethostbyname(remote_host)
        port_number = sys.argv[2]
        sock.connect((remote_host_ip, int(port_number)))
        
        with open("server_public_Key.pem","rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
    
    
        key = Fernet.generate_key() 
        fernet_obj = Fernet(key)
        encrypted_K = rsa.encrypt(key, public_key)
        
        sock.send(encrypted_K)
        data = "0"
        while data == "0":
            username = input("Enter your ID: ")
            password = getpass.getpass("Enter your password: ")
            credentials = username + " " + password
            encrypted_credentials = fernet_obj.encrypt(credentials.encode())
            sock.send(encrypted_credentials)
            
            data = sock.recv(1).decode()
            if data == "0":
                print("ID and password are incorrect")
            elif data == "1":
                print("ID and password are correct")
            else:  
                print("Unexpected response from the server. Please try again.")   

       
        while True:
            print("Please select one of the following actions (enter 1, 2, or 3):")
            print("1. Transfer money")
            print("2. Check account balance")
            print("3. Exit")

            choice = input("Please enter your choice: ")
            if choice not in ["1", "2", "3"]:
                print("Incorrect input. Please try again.")
            else:
                sock.send(choice.encode())          
            if choice == "1":
                while True:
                    print("Please select an account (enter 1 or 2):")
                    print("1. Savings")
                    print("2. Checking")
                    account_option = input("Enter your choice: ")
                    if account_option not in ["1", "2"]:
                        print("Incorrect input. Please try again.")
                    else:
                        sock.send(account_option.encode())
                        break

                receiver = input("Enter the receiver's ID : ")
                amount = input("Enter the amount to be transferred : ")
                transfer = f"{receiver}|{amount}"
               
                sock.send(transfer.encode())
                response = sock.recv(1024).decode()


                if response == "1":
                    print("Your transaction is successful.")
                elif response == "0":  
                    print("Your transaction is unsuccessful.")
                elif response == "recipient_not_exist":
                    print("The recipient's ID does not exist.")
                elif response == "insufficient_funds":
                    print("Your account does not have enough funds.")
                elif response == "sender_and_recipient_are_same":
                    print("Sender and Recipient are same.")
            elif choice == "2":   
                balances_response = sock.recv(1024).decode()
                print(balances_response)
            elif choice == "3":
                sock.send(choice.encode())
                sock.close()
                print("Connection closed. Exiting...")
                break    