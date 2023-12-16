import hashlib
import getpass
import datetime

while True:
    user_id = input("Enter your ID: ")
    if not user_id.islower() or any(char.isdigit() for char in user_id):
        print("The ID should only contain lower-case letters.")
        continue

    # ID Check
    try:
        with open("hashpasswd", "r") as file:
            existing_ids = [line.split()[0] for line in file]
            if user_id in existing_ids:
                print("The ID already exists.")
                another_entry = input("Would you like to enter another ID and password (Y/N)? ").strip().lower()
                if another_entry != 'y':
                    break
                else:
                    continue
    except FileNotFoundError:
        # Generates the file if it doesn't exist
        pass

    while True:    
        password = getpass.getpass("Enter your password: ")
        if len(password) < 8:
            print("The password should contain at least 8 characters.")
            continue
        else:
            break    

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("hashpasswd", "a") as file:
        file.write(f"{user_id} {hashed_password} {current_time}\n")

    another_entry = input("Would you like to enter another ID and password (Y/N)? ").strip().lower()
    if another_entry != 'y':
        break
