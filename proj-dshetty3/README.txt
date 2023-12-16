Name:		Disha Shetty
B-Number:	B00965377
Email:	dshetty3@binghamton.edu
Programming Language: Python

Code for performing encryption/decryption: RSA used
Symmetric Key - Fernet

openssl genpkey -algorithm RSA -out private.key
openssl req -new -key private.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey private.key -out new.pem
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > sym_key.key
no requirement of client keys
openssl genpkey -algorithm RSA -out client_private_Key.pem
openssl rsa -pubout -in client_private_Key.pem -out client_public_Key.pem


Code is tested on remote.cs.binghamton.edu and placed in folder named proj-dshetty3 in the following 
directory: /home/dshetty3/proj-dshetty3

Dependencies:
Since RSA could not be installed in VM (no permissions), I created a venv named proj-dshetty3
Commands:
Navigate to /home/dshetty3/CS558-23f/
python3 -m venv proj-dshetty3
source proj-dshetty3/bin/activate
pip install rsa
pip install cryptography

Process for executing the code:
1. Navigate to /home/dshetty3/CS558-23f/proj-dshetty3 terminal on remote.cs
2. Execute the following command for starting server: python3 bank.py 8281 (any port number)
3. In a new terminal for client, navigate to Navigate to /home/dshetty3/CS558-23f/proj-dshetty3 on remote.cs
4. Execute the following command for server: python3 atm.py remote0x 8281 (x can be from 0 to 7)
(Mention the remote host name where server socket is running)
5. Once connection is established between client and server, you can run the necessary test cases.


References:
1) RSA Private & Public Key Encryption in Python - https://www.youtube.com/watch?v=n0uJsqFGO4k&ab_channel=NeuralNine


