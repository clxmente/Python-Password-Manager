import sys

from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import *

class Manager:
    """
    Arguments: 
    \tobj {DataManip}
    \tfilename {str}
    \tmaster_pass {str}
    """
    def __init__(self, obj: DataManip, filename: str, master_pass: str):
        self.obj_ = obj
        self.filename_ = filename
        self.master_pass_ = master_pass

    def begin(self):
        try:
            # TODO: test and try to break after all options finished
            choice = self.menu_prompt()
        except UserExits:
            raise UserExits

        if choice == '3': # User Exits
            raise UserExits

        if choice == '1': # add or update a password
            # NOTE: fully tested already
            try:
                self.update_db()
                return self.begin()
            except UserExits:
                raise UserExits
        
        elif choice == '2': # look up a stored password
            # NOTE: fully tested already
            try:
                string = self.load_password()
                website = string.split(':')[0]
                password = string.split(':')[1]
                print(colored(f"Password for {website}: {password}", "yellow"))
                
                return self.begin()
            except UserExits:
                raise UserExits
            except PasswordFileDoesNotExist:
                print(colored(f"{self.obj_.x_mark_} DB not found. Try adding a password {self.obj_.x_mark_}", "red"))
                return self.begin()

        elif choice == '4': # Delete DB/Passwords
            try:
                self.delete_db(self.master_pass_)
            except MasterPasswordIncorrect:
                print(colored(f"{self.obj_.x_mark_} Master password is incorrect {self.obj_.x_mark_}", "red"))
                return self.delete_db(self.master_pass_)
            except UserExits:
                raise UserExits
                
                


    def menu_prompt(self):
        """Asks user for a choice from Menu
        
        Raises:
        \tUserExits: User exits on choice prompt
        
        Returns:
        \tstr -- Users choice
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
        \twebsite {str} -- website for password
        
        Raises:
        \tUserExits: User exits on loop prompt
        
        Returns:
        \tstr -- A randomly generated password
        """

        try:
            generated_pass = self.obj_.generate_password()
            print(colored(generated_pass, "yellow"))

            loop = input("Generate a new password? (Y/N): ")
            if loop.lower().strip() == "exit":
                raise UserExits
            elif (loop.lower().strip() == 'y') or (loop.strip() == "") :
                return self.__return_generated_password(website) # recursive call
            elif loop.lower().strip() == 'n':
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
        \tUserExits: User enters exit at website prompt or generate prompt
        """

        website = input("Enter the website for which you want to store a password (ex. google.com): ")
        if website.lower() == "":
            #raise EmptyField
            self.update_db()
        elif website.lower().strip() == "exit":
            raise UserExits
        else:
            gen_question = input("Do you want to generate a password for {} ? (Y/N): ".format(website))
            if gen_question.strip() == "":
                #raise EmptyField
                self.update_db()
            elif gen_question.lower().strip() == "exit":
                raise UserExits
            elif gen_question.lower().strip() == 'n': # user wants to manually enter a password
                password = input("Enter a password for {}: ".format(website))
                if password.lower().strip() == "exit":
                    raise UserExits
                else:
                    self.obj_.encrypt_data(self.filename_, password, self.master_pass_, website)
                    
            elif gen_question.lower().strip() == 'y':
                password = self.__return_generated_password(website)
                self.obj_.encrypt_data("db/passwords.json", password, self.master_pass_, website)
    
    def load_password(self):
        """Loads a string of websites stored and asks user to enter a 
        website, then decrypts password for entered website
        
        Raises:
        \tPasswordFileDoesNotExist: DB is not initialized
        \tUserExits: User enters exit on website prompt
        
        Returns:
        \tstr -- string formatted in website:password
        """

        print(colored("Current Passwords Stored:", "yellow"))
        spinner = Halo(text=colored("Loading Passwords", "yellow"), color="yellow", spinner=self.obj_.dots_)
        
        try:
            lst_of_passwords = self.obj_.list_passwords(self.filename_)
        except PasswordFileIsEmpty:
            lst_of_passwords = "--There are no passwords stored.--"
            print(colored(lst_of_passwords, "yellow"))
            return self.begin()
        except PasswordFileDoesNotExist:
            print(colored(f"{self.obj_.x_mark_} DB not found. Try adding a password {self.obj_.x_mark_}", "red"))
            return self.begin()

        spinner.stop()

        print(colored(lst_of_passwords, "yellow"))

        website = input("Enter website for the password you want to retrieve: ")

        if website.lower().strip() == "exit":
            raise UserExits
        elif website.strip() == "":
            return self.load_password()
        else:
            try:
                plaintext = self.obj_.decrypt_data(self.master_pass_, website, self.filename_)
            except PasswordNotFound:
                print(colored(f"{self.obj_.x_mark_} Password for {website} not found {self.obj_.x_mark_}", "red"))
                return self.load_password()
            except PasswordFileDoesNotExist:
                print(colored(f"{self.obj_.x_mark_} DB not found. Try adding a password {self.obj_.x_mark_}", "red"))
                return self.begin()
            
            # see https://pypi.org/project/clipboard/ for copying to clipboard
            final_str = f"{website}:{plaintext}"

            return final_str

    def delete_db(self, stored_master):
        """Menu Prompt to Delete DB/Passwords
        
        Arguments:
        \tstored_master {str} -- Used to authenticate, compared with inputted master password
        
        Raises:
        \tPasswordFileDoesNotExist: Password file not initialized
        """

        confirmation = input("Are you sure you want to delete the password file? (Y/N)")
        if confirmation.lower().strip() == 'y':
            entered_master = input("Enter your master password to delete all stored passwords: ")
            if entered_master.lower().strip() == "exit":
                raise UserExits
            else:
                try:
                    self.obj_.delete_db(self.filename_, stored_master, entered_master)
                    print(colored(f"{self.obj_.checkmark_} Password Data Deleted successfully. {self.obj_.checkmark_}", "green"))
                    return self.begin()
                except MasterPasswordIncorrect:
                    raise MasterPasswordIncorrect
                except PasswordFileDoesNotExist:
                    print(colored(f"{self.obj_.x_mark_} DB not found. Try adding a password {self.obj_.x_mark_}", "red"))
                    return self.begin()
        elif confirmation.lower().strip() == 'n':
                print(colored("Cancelling...", "red"))
                return self.begin()
        elif confirmation.lower().strip() == "exit":
            raise UserExits
        elif confirmation.strip() == "":
            return self.delete_db(stored_master)