import os
import json
import sys

from os.path import isfile
from modules.encryption import DataManip
from modules.exceptions import *
from hashlib import sha256
from termcolor import colored
from halo import Halo

def exit_program():
    print(colored("Goodbye!", "green"))
    sys.exit()

def start(obj: DataManip):
    if os.path.isfile("db/masterpassword.json"):
        with open("db/masterpassword.json", 'r') as jsondata:
            jfile = json.load(jsondata)

        stored_master_pass = jfile["Master"] # load the saved hashed password

        master_password = input("Enter your Master Password: ")

        # compare the two hashes of inputted password and stored
        spinner = Halo(text=colored("Unlocking", "green"), color="green", spinner=obj.dots_)
        if sha256(master_password.encode("utf-8")).hexdigest() == stored_master_pass:
            print(colored("\n Enter 'exit' at any point to exit.\n", "magenta"))
            print(colored("1) Add/Update a password", "blue"))
            print(colored("2) Look up a stored password", "blue"))
            print(colored("3) Exit program", "blue"))
            print(colored("4) Erase all passwords", "red"))
            choice = input("Enter a choice: ")

            if choice == "1": # add or update a password
                website = input("Enter the website for which you want to store a password. (ex. google.com): ")
                if website.lower() == "exit":
                    exit_program()
                else:
                    gen_question = input("Do you want to generate a password for {} ? (Y/N): ".format(website))
                    if gen_question.lower() == 'n':
                        password = input("Enter a password for {}: ".format(website))
                        obj.encrypt_data("db/passwords.json", password, master_password, website)
                    elif gen_question.lower() == 'y':
                        try:
                            generated_pass = obj.generate_password()
                            obj.encrypt_data("db/passwords.json", generated_pass, master_password, website)
                        except PasswordNotLongEnough:
                            print(colored("Password is not long enough, please enter a number above 8."))
                            exit_program()
                        except (UserExits, EmptyField):
                            exit_program()
                    else:
                        print(colored("Invalid option.", "red"))
                        exit_program()
    else: # First time running program: create a master password
        os.mkdir("db/")
        print(colored("To start, we'll have you create a master password. Be careful not to lose it as it is unrecoverable.", "green"))
        master_password = input("Create a master password for the program: ")

        spinner = Halo(text=colored("initializing base...", "green"), color="green", spinner=obj.dots_)
        hash_master = sha256(master_password.encode("utf-8")).hexdigest()
        jfile = {"Master": {}}
        jfile["Master"] = hash_master
        with open("db/masterpassword.json", 'w') as jsondata:
            json.dump(jfile, jsondata, sort_keys=True, indent=4)
        spinner.stop()
        print(colored("Thank you! Restart the program and enter your master password to begin.", "green"))

if __name__ == "__main__":
    obj = DataManip()
    start(obj)

# TODO: options 2-4, also loop the program after options.
