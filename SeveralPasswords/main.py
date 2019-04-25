import random
import time
import os
import json
from Crypto.Cipher import AES
from halo import Halo
from os.path import isfile


alphabetLower = "abcdefghijklmnopqrstuvwxyz"
alphabetUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specialChar = "!@#$%^&*()-_"

dots = {"interval": 80, "frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]}

def generate_password():
    password = []

    length = input("How many characters do you want your password to be? ")
  
    if int(length) < 8:
        print("It is recommended you have a password of at least 8 characters")
        generate_password()
    
    else:
        for i in range(0, int(length)):
            password.append(random.choice(random.choice([alphabetLower, alphabetUpper, digits, specialChar]))) 
    
        finalPass = "".join(password)

        spinner = Halo(text="Generating Password", spinner=dots, color="green")
        spinner.start()
        time.sleep(1)
        spinner.stop()

        print(finalPass)
        loop = input("Generate a new password? (Y/N) ")

        if loop.lower() == "y":
            generate_password()
        else:
            savePass = input("Would you like to save the password? (Y/N) ")
            if savePass.lower() == 'y':
                #save password to database
                spinner = Halo(text="Saving", spinner=dots, color="green")
                spinner.start()
                time.sleep(1)
                spinner.stop()
                print("Thank you!")
                pass
            else:
                spinner = Halo(text="Exiting", spinner=dots, color="red")
                spinner.start()
                time.sleep(1)
                spinner.stop()
                print("Goodbye!")

def start():
    print("1) Add/Update a password in the database")
    print("2) Look up a stored password")
    print("3) Erase all passwords")
    beginProgram = input("Enter a choice: ")

    if beginProgram == "1": #add or update password
        pass
    elif beginProgram == "2":
        #look up a stored password
        pass
    elif beginProgram == "3":
        #first ask the user if they are sure they want to delete the database
        #prompt them for the password
        #delete the data
        pass
		
		
		
"""
		Decrypting the data isn't an option. JSON doesn't support the encrypted data type so the encoded messages can't be stored in the json file.




def encrypt_data(data, master_pass):
    key = master_pass.encode('utf-8') #must be 16 bytes 
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce #A value that must never be reused for any other encryption done with this key (save alongside encrypted password?)
    #print(nonce)

    if os.path.isfile("passwords.json"):
        try:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile["reddit.com"]["nonce"] = str(nonce)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
        except KeyError:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile["reddit.com"] = {}
            jfile["reddit.com"]["nonce"] = str(nonce)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)

    else:
        jfile = {"reddit.com": {}}
        jfile["reddit.com"]["nonce"] = str(nonce)
        with open('passwords.json', 'w') as jsondata:
            json.dump(jfile, jsondata, sort_keys=True, indent=4)



    data_to_encrypt = data.encode('utf-8') #password that would be encrypted where *data* is the password
    ciphertext = cipher.encrypt(data_to_encrypt)
    print(ciphertext)

def decrypt_data(key, encrypted_data):
    if os.path.isfile('passwords.json'):
        try:
            with open('passwords.json', 'r') as jdata:
                jfile = json.load(jdata)
            nonce = jfile["reddit.com"]["nonce"].encode('utf-8')
        except KeyError:
            pass



    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_data)
    print(plaintext)

encrypt_data('myRedditPassword', '1234567891234567')

decrypt_data('1234567891234567', b'!:\xdc*\x9e\x00.\xb1\x89I\x0e\x8am+\x9a\xa1')

"""
