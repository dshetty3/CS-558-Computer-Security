Name: Disha Shetty
B-Number: B00965377
Email: dshetty3@binghamton.edu


This assignment is tested in remote.cs and placed in the folder p3-dshetty3 in the following directory /home/dshetty3
How to run/test the code:
1) Create a genpasswd.py file and run the following commands python3 genpasswd.py 
    Will ask for ID and Password (ID should be lowercase and passward should be atleast 8 characters long)
    after that it will be saved in the hashpasswd file (.txt file)
2) Navigate to /home/dshetty3/CS558-23f/p3-dshetty3/Server in terminal on remote.cs
    Execute the following command: python3 serv.py <port_number> (use 5377 i.e. python3 serv.py 5377)
    Server will be listening on the said port given in command - line argument
3) Navigate to /home/dshetty3/CS558-23f/p3-dshetty3/Client in terminal on remote.cs
    Execute the following command: python3 cli.py remote0x.cs.binghamton.edu 5377 (x can be from 0 to 7)
    Client will establish connection successfully with server and  prompt to enter ID and password.
4) Once ID and password is sent, the server will receive them and computes the hash of the password against the file in the hashpasswd. 
    If there is a match, it prints "Correct ID and Password to the client, else it prints "The ID/password is incorrect", and will ask to re-enter it.
     
NOTE: PEM pass phrase should be entered as 1234.     