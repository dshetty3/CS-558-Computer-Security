import sys

def check_key(keylength, key):
    if len(key) != keylength:
        # Error handle 1
        print("<keylength> must match the length of <key>.")
        sys.exit(1)
    for i in range(1, keylength + 1):
        if str(i) not in key:
            #Error handle 2
            print("<key> must include all digits from 1 to <keylength> with each digit occurring exactly once.")
            sys.exit(1)    

def check_inputfile(inputfile):
    with open(inputfile, 'r') as file:
        data = file.read()
        if not data.isalnum() or any(char.isupper() for char in data):
            #Error handle 3
            print("<inputfile> must contain only lowercase letters (a-z) or digits (0-9).")
            sys.exit(1)
          
#Encryption starts here
def encrypt(keylength, key, inputfile, outputfile):
    check_key(keylength, key)
    check_inputfile(inputfile)

    with open(inputfile, 'r') as infile, open(outputfile, 'w') as outfile:
        data = infile.read()

        pad_len = keylength - (len(data) % keylength)

        if pad_len != keylength:
            data += 'z' * pad_len

        encrypted_text = [''] * keylength

        for i in range(len(data)):
            j = i % keylength
            encrypted_text[j] += data[i]

        cipher_text = ''
        for digit in key:
            index = int(digit) - 1
            cipher_text += encrypted_text[index]

        outfile.write(cipher_text)

#Decryption starts here
def decrypt(keylength, key, inputfile, outputfile):
    check_key(keylength, key)
    check_inputfile(inputfile)

    with open(inputfile, 'r') as infile, open(outputfile, 'w') as outfile:
        data = infile.read()

        block_size = len(data) // keylength
        decrypted_text = [''] * keylength

        for i in range(keylength):
            start = i * block_size
            end = start + block_size
            decrypted_text[int(key[i]) - 1] = data[start:end]

        max_length = len(decrypted_text[0])
        plain_text = ''

        for i in range(max_length):
            for j in range(keylength):
                if i < len(decrypted_text[j]):
                    plain_text += decrypted_text[j][i]

        outfile.write(plain_text)

if len(sys.argv) != 6:
    print(" Input should have 5 arguments: <keylength> <key> <inputfile> <outputfile> <enc/dec>")
    sys.exit(1)

keylength = int(sys.argv[1])
key = sys.argv[2]
inputfile = sys.argv[3]
outputfile = sys.argv[4]
operation = sys.argv[5]

if operation == "enc":
    encrypt(keylength, key, inputfile, outputfile)
    print("Encryption complete.")
elif operation == "dec":
    decrypt(keylength, key, inputfile, outputfile)
    print("Decryption complete.")
else:
    print("Invalid operation. Use 'enc' for encryption or 'dec' for decryption.")
    sys.exit(1)
