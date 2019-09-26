# Python Password Manager
>Note: This password manager was made as a project and is NOT intended for actual use. Please use more sophisticated and well-tested/trusted password managers to store sensitive data.

## AES Encryption

The encryption method used in this program comes from the python library [PyCryptoDome](https://pypi.org/project/pycryptodome/). This program uses AES encryption methods to store sensitive data (in this case passwords) into a json file.

## Hash Verification
 To authenticate the user, they are prompted to create a master password (that is also used to decrypt data) which is then stored using a SHA256 Hash Function and is verified throughout sensitive parts of the program. Whenever the user is prompted to verify their master password, the password they enter is compared to the hash of the stored master password and access if granted if the two hashes match.
 ```Python
 if os.path.isfile("masterpassword.json"): # loading json file with stored password.
       with open("masterpassword.json", "r") as jsondata:
           jfile = json.load(jsondata)

       verify_pass = jfile["Master"] # retrieving stored hash and saving to a variable.

       master_password = input("Enter your MASTER password: ")
       # compaing the two hashes
       if sha256(master_password.encode('utf-8')).hexdigest() == verify_pass:
         #rest of program executes
```
