import sys

from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import *

class Manager:
    """
    Arguments: 
        obj {DataManip}
        filename {str}
        master_pass {str}
    """
    def __init__(self, obj: DataManip, filename: str, master_pass: str):
        self.obj_ = obj
        self.filename_ = filename
        self.master_pass_ = master_pass

    def menu_prompt(self):
        """Asks user for a choice from Menu
        
        Raises:
            UserExits: User exits on choice prompt
        
        Returns:
            str -- Users choice
        """
        print(colored("\n\t*Enter 'exit' at any point to exit.*\n", "magenta"))
        print(colored("1) Add/Update a password", "blue"))
        print(colored("2) Look up a stored password", "blue"))
        print(colored("3) Exit program", "blue"))
        print(colored("4) Erase all passwords", "red"))

        choice = input("Enter a choice: ")

        if choice == "":
            return self.menu_prompt() # recursive call
        elif choice == "exit":
            raise UserExits
        else:
            return choice.strip()

    def __return_generated_password(self, website):
        """Returns a generated password
        
        Arguments:
            website {str} -- website for password
        
        Raises:
            UserExits: User exits on loop prompt
        
        Returns:
            str -- A randomly generated password
        """

        try:
            generated_pass = self.obj_.generate_password()
            print(colored(generated_pass, "yellow"))

            loop = input("Generate a new password? (Y/N): ")
            if loop.lower() == "exit":
                raise UserExits
            elif (loop.lower() == 'y') or (loop == "") :
                return self.__return_generated_password(website) # recursive call
            elif loop.lower() == 'n':
                return generated_pass
        except (PasswordNotLongEnough, EmptyField):
            print(colored("Password length invalid.", "red"))
            return self.__return_generated_password(website)
        except UserExits:
            print(colored("Exiting...", "red"))
            sys.exit()


    def update_db(self): # option 1 on main.py
        """Add or update a password in the DB
        
        Raises:
            UserExits: User enters exit at website prompt or generate prompt
        """

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
                self.obj_.encrypt_data(self.filename_, password, self.master_pass_, website)
            elif gen_question.lower() == 'y':
                password = self.__return_generated_password(website)
                self.obj_.encrypt_data("db/passwords.json", password, self.master_pass_, website)
    
    def load_password(self):
        print(colored("Current Passwords Stored:", "yellow"))
        spinner = Halo(text=colored("Loading Passwords", "yellow"), color="yellow", spinner=self.obj_.dots_)
        
        try:
            lst_of_passwords = self.obj_.list_passwords(self.filename_)
        except PasswordFileIsEmpty:
            lst_of_passwords = "--There are no passwords stored.--"
        except PasswordFileDoesNotExist:
            raise PasswordFileDoesNotExist

        spinner.stop()

        print(colored(lst_of_passwords, "yellow"))

        website = input("Enter website for the password you want to retrieve: ")

        if website.lower() == "exit":
            raise UserExits
        elif website == "":
            raise EmptyField
        else:
            try:
                plaintext = self.obj_.decrypt_data(self.master_pass_, website, self.filename_)
            except PasswordNotFound:
                print(colored(f"{self.obj_.x_mark_} Password for {website} not found {self.obj_.x_mark_}", "red"))
                return self.load_password()
            except PasswordFileDoesNotExist:
                raise PasswordFileDoesNotExist
            
            # see https://pypi.org/project/pyperclip/ for copying to clipboard
            final_str = f"Password for {website}: {plaintext}"

            return final_str

    

