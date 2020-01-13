# Python Password Manager
>Note: This password manager was made as a project and is NOT intended for actual use. Please use more sophisticated and well-tested/trusted password managers to store sensitive data.

## Demo

[![asciicast](https://asciinema.org/a/tEGTsXmEMJALLhuYljnRWf8Oh.svg)](https://asciinema.org/a/tEGTsXmEMJALLhuYljnRWf8Oh)

## AES Encryption

The encryption method used in this program comes from the python library [PyCryptoDome](https://pypi.org/project/pycryptodome/). This program uses AES encryption methods to store sensitive data (in this case passwords) into a json file.

## Hash Verification
 To authenticate the user, they are prompted to create a master password (that is also used to decrypt data) which is then stored using a SHA256 Hash Function and is verified at login. Whenever the user is prompted to verify their master password, the password they enter is compared to the hash of the stored master password and access if granted if the two hashes match.
 ```python
 if os.path.isfile("db/masterpassword.json"): # loading json file with stored password.
       with open("db/masterpassword.json", 'r') as jsondata:
           jfile = json.load(jsondata)

       stored_master_pass = jfile["Master"] # retrieving stored hash and saving to a variable.
       master_password = getpass.getpass("Enter your Master password: ") # asking user to enter their master password
       
       # comparing the two hashes
       if sha256(master_password.encode('utf-8')).hexdigest() == stored_master_pass:
         #rest of program executes
```
## Changelog
Python-Password-Manager has been completely rewritten to be more object-oriented and abstract even more of the methods found in the original version. 

#### Notable Changes:
* Object-Oriented Design:
  * Creation of [DataManip Class](./modules/encryption.py):
    * Handles all backend processes regarding encryption, decryption, and DB functions.
  * Creation of [Manager Class](./modules/menu.py):
    * Uses DataManip methods to provide the CLI interface seen in the Demo.
  * [Custom Exceptions](./modules/exceptions.py):
    * Better handling of errors.
* General Improvements:
  * Now returns user to specific points of the program after errors where as before the entire program would restart.
  * Echo mode is set to off when Master Password is being entered.
  * Added two options to menu:
    * Delete a single password
    * Specific options to delete ONLY passwords and another option to completely wipe all data including master password.
  * Option to copy retrieved password to clipboard
  * General code/implementation improvements

# Vulnerability
As mentioned at the top, this was made as a project and not intended for actual use. Below I demonstrate what any expert hacker can accomplish by exploiting a vulnerability. Just kidding, anyone can do this. Since the files are stored locally, they can easily be deleted without needing to enter any credentials and consequently all stored passwords are gone along with other data.

<a href="https://youtu.be/Jy-c8QbzJFI" target="_blank"> <img src="./vuln.gif" width="800"> </a>
