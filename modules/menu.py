import sys

from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import *

class Manager:
    def __init__(self, obj: DataManip, filename: str, master_pass: str):
        self.obj_ = obj
        self.filename_ = filename
        self.master_pass_ = master_pass

    def save_generated_password(self, website):
        try:
            generated_pass = self.obj_.generate_password()
            print(colored(generated_pass, "yellow"))

            loop = input("Generate a new password? (Y/N): ")
            if loop.lower() == "exit":
                raise UserExits
            elif (loop.lower() == 'y') or (loop == "") :
                self.save_generated_password(website) # recursive call
            elif loop.lower() == 'n':
                return generated_pass
        except (PasswordNotLongEnough, EmptyField):
            self.save_generated_password(website)
        except UserExits:
            print(colored("Exiting...", "red"))
            sys.exit()


    def update_db(self): # option 1 on main.py
        website = input("Enter the website for which you want to store a password (ex. google.com): ")
        if website.lower() == "":
            #raise EmptyField
            self.update_db()
        elif website.lower() == "exit":
            raise UserExits
        else:
            gen_question = input("Do you want to generate a password for {} ? (Y/N): ".format(website))
            if gen_question == "":
                #raise EmptyField
                self.update_db()
            elif gen_question == "exit":
                raise UserExits
            elif gen_question.lower() == 'n':
                password = input("Enter a password for {}: ".format(website))
                obj_.encrypt_data(self.filename_, password, self.master_pass_, website)
            elif gen_question.lower() == 'y':
                try:
                    generated_pass = self.obj_.generate_password()
                    print(colored(generated_pass, "yellow"))
                    self.obj_.encrypt_data(self.filename_, generated_pass, self.master_pass_, website)
                except (PasswordNotLongEnough, EmptyField):
                    print(colored("Password length invalid.", "red"))
                    self.update_db()
                except UserExits:
                    print(colored("Exiting...", "red"))
                    sys.exit()
