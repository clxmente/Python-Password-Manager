import os
import json
import sys

from os.path import isfile
from hashlib import sha256
from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import UserExits, PasswordFileDoesNotExist
from modules.menu import Manager

def exit_program():
    print(colored("Exiting...", "red"))
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
            # create instance of Manager class
            menu = Manager(obj, "db/passwords.json", master_password)

            try:
                # TODO: test and try to break
                choice = menu.menu_prompt()
            except UserExits:
                exit_program()

            if choice == "1": # add or update a password
                try:
                    menu.update_db()
                except UserExits:
                    exit_program()
            elif choice == "2": # look up a stored password
                try:
                    password = menu.load_password()
                    print(colored(password, "yellow"))
                except UserExits:
                    exit_program()
                except PasswordFileDoesNotExist:
                    print(colored("DB is empty, please create a password first", "red"))
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
