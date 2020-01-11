import json
import string
import os
import random

from Crypto.Cipher import AES
from halo import Halo
from termcolor import colored

from modules.exceptions import *



class DataManip:
    def __init__(self):
        self.dots_ = {"interval": 80, "frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]}
        self.checkmark_ = "\u2713"
        self.x_mark_ = "\u2717"
        self.specialChar_ = "!@#$%^&*()-_"

    def __save_password(self, filename, data, nonce, website):
        """Saves password to DB
        
        Arguments:
            filename {str} -- DB to save to
            data {str} -- password that will be saved
            nonce {hexadecimal} -- converted from byte type to hexadecimal as byte type is not supported in JSON
            website {str} -- name of the website for the given password
        """               

        spinner = Halo(text=colored("Saving", "green"), spinner=self.dots_, color="green")
        spinner.start()
        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as jsondata:
                    jfile = json.load(jsondata)
                jfile[website]["nonce"] = nonce
                jfile[website]["password"] = data
                with open(filename, 'w') as jsondata:
                    json.dump(jfile, jsondata, sort_keys=True, indent=4)
            except KeyError:
                with open(filename, 'r') as jsondata:
                    jfile = json.load(jsondata)
                jfile[website] = {}
                jfile[website]["nonce"] = nonce
                jfile[website]["password"] = data
                with open(filename, 'w') as jsondata:
                    json.dump(jfile, jsondata, sort_keys=True, indent=4)
        else: # initialize the file in case it doesn't exist off the start
            jfile = {website: {}}
            jfile[website]["nonce"] = nonce
            jfile[website]["password"] = data
            with open(filename, 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
        spinner.stop()
        print(colored("{} Saved successfully. Thank you!".format(self.checkmark_)))



    def encrypt_data(self, filename, data, master_pass, website):
        """Encrypt and save the data to a file using master password as the key
        
        Arguments:
            filename {str}
            data {str} -- password to save
            master_pass {str}
            website {str} -- website to store password
        """        

        """Concatenated extra characters in the case that the master password
        is less than 16 characters. However, this isn't a big safety trade off
        as the full length master password is hashed and checked for."""
        concatenated_master = master_pass + "================"

        key = concatenated_master[:16].encode("utf-8")

        cipher = AES.new(key, AES.MODE_EAX)

        """A value that must never be reused for any other encryption done with
        this key saved alongside encrypted password. Converted to hexadecimal
        to be saved in DB. Later converted back to bytes to decode data"""
        nonce = cipher.nonce.hex()

        data_to_encrypt = data.encode("utf-8")
        # again, bytes is invalid data for JSON so we convert it
        encrypted_data = cipher.encrypt(data_to_encrypt).hex()

        self.__save_password(filename, encrypted_data, nonce, website)

    def decrypt_data(self, master_pass, website, filename):
        """Return a decrypted password as a string.
        
        Arguments:
            master_pass {str} -- key
            website {str} -- The password being returned is from this website
            filename {str} -- database in which the password is stored.
        
        Raises:
            PasswordNotFound: Password is not located in DB
            PasswordFileDoesNotExist: The db is not initiated
        
        Returns:
            str -- decrypted password
        """    

        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as jdata:
                    jfile = json.load(jdata)
                nonce = bytes.fromhex(jfile[website]["nonce"])
                password = bytes.fromhex(jfile[website]["password"])
            except KeyError:
                raise PasswordNotFound
        else:
            raise PasswordFileDoesNotExist
        # add extra characters and take first 16 to make sure key is right.
        formatted_master_pass = master_pass + "================"
        master_pass_encoded = formatted_master_pass[:16].encode("utf-8")
        cipher = AES.new(master_pass_encoded, AES.MODE_EAX, nonce = nonce)
        plaintext_password = cipher.decrypt(password).decode("utf-8")

        return plaintext_password

    def generate_password(self):
        """Generates a complex password
        
        Raises:
            UserExits: user types "exit" in length
            EmptyField: user leaves length field empty
            PasswordNotLongEnough: raised when user enters a length below 8
        
        Returns:
            str -- complex password
        """        

        # needs rewrite to get rid of spinner for GUI.
        password = []
        length = input("Enter Length for Password (At least 8): ")

        if length.lower() == "exit":
            raise UserExits
        elif length == "":
            raise EmptyField
        elif int(length) < 8:
            raise PasswordNotLongEnough
        else:
            # generating a password
            spinner = Halo(text=colored("Generating Password", "green"), spinner=self.dots_, color="green")
            spinner.start()
            for i in range(0, int(length)):
                #choose character from one of the lists randomly
                password.append(random.choice(random.choice([string.ascii_lowercase, string.ascii_uppercase, string.digits, self.specialChar_])))

            finalPass = "".join(password)
            spinner.stop()

            return finalPass
    
    def list_passwords(self, filename):
        """Loads a list of websites in DB
        
        Arguments:
            filename {str} -- DB file
        
        Raises:
            PasswordFileIsEmpty: No Passwords stored in DB
            PasswordFileDoesNotExist: Password File Not found
        
        Returns:
            str -- List of Passwords
        """
        
        if os.path.isfile(filename):
            with open(filename, 'r') as jsondata:
                pass_list = json.load(jsondata)
            
            passwords_lst = ""
            for i in pass_list:
                passwords_lst += "--{}\n".format(i)
            
            if passwords_lst == "":
                raise PasswordFileIsEmpty
            else:
                return passwords_lst
        else:
            raise PasswordFileDoesNotExist
