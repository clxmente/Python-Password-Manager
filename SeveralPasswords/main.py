import random
import time
import os
import json

from halo import Halo
from os.path import isfile
from termcolor import colored


alphabetLower = "abcdefghijklmnopqrstuvwxyz"
alphabetUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specialChar = "!@#$%^&*()-_"

checkmark = "\u2713"
x_mark = "\u2717"

dots = {"interval": 80, "frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]}

def generate_password(website):
    password = []

    length = input("How many characters do you want your password to be? (At least 8) ")
  
    if int(length) < 8:
        print(colored("{} A password of at least 8 characters is required".format(x_mark), "red"))
        restart_program()
    
    else:
        for i in range(0, int(length)):
            password.append(random.choice(random.choice([alphabetLower, alphabetUpper, digits, specialChar]))) 
    
        finalPass = "".join(password)

        spinner = Halo(text=colored("Generating Password", "green"), spinner=dots, color="green")
        spinner.start()
        time.sleep(1)
        spinner.stop()

        print(finalPass)
        loop = input("Generate a new password? (Y/N) ")

        if loop.lower() == "y":
            generate_password(website)
        else:
            savePass = input("Would you like to save the password? (Y/N) ")
            if savePass.lower() == 'y':
                #save password to database
                spinner = Halo(text=colored("Saving", "green"), spinner=dots, color="green")
                spinner.start()

                if os.path.isfile("passwords.json"):
                    try:
                        with open('passwords.json', 'r') as jsondata:
                            jfile = json.load(jsondata)
                        jfile[website]["password"] = finalPass
                        with open('passwords.json', 'w') as jsondata:
                            json.dump(jfile, jsondata, sort_keys=True, indent=4)
                    except KeyError:
                        with open('passwords.json', 'r') as jsondata:
                            jfile = json.load(jsondata)
                        jfile[website] = {}
                        jfile[website]["password"] = finalPass
                        with open('passwords.json', 'w') as jsondata:
                            json.dump(jfile, jsondata, sort_keys=True, indent=4)

                else:
                    jfile = {website: {}}
                    jfile[website]["password"] = finalPass
                    with open('passwords.json', 'w') as jsondata:
                        json.dump(jfile, jsondata, sort_keys=True, indent=4)




                time.sleep(1)
                spinner.stop()
                print(colored("{} Saved successfully. Thank you!".format(checkmark), "green"))
            else:
                exit_program()

def save_password(password, website):
    if os.path.isfile("passwords.json"):
        try:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile[website]["password"] = password
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
        except KeyError:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile[website] = {}
            jfile[website]["password"] = password
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)

    else:
        jfile = {website: {}}
        jfile[website]["password"] = password
        with open('passwords.json', 'w') as jsondata:
            json.dump(jfile, jsondata, sort_keys=True, indent=4)

    spinner = Halo(text=colored("Saving", "green"), spinner=dots, color="green")
    spinner.start()
    time.sleep(1)
    spinner.stop()
    print(colored("{} Saved successfully. Thank you!".format(checkmark), "green"))


def start():
    print(colored("1) Add/Update a password in the database", 'blue'))
    print(colored("2) Look up a stored password", 'blue'))
    print(colored("3) Exit program", 'blue' ))
    print(colored("4) Erase all passwords", 'red' ))
    beginProgram = input("Enter a choice: ")

    if beginProgram == "1": #add or update password
        website = input("Enter the website for which you want to store a password. (EX: google.com): ")
        if website.lower() == 'exit':
            exit_program()

        else:
            gen_question = input("Do you want to generate a password for {} ? (Y/N): ".format(website))

            if gen_question.lower() == 'n':
                password = input("Enter a password for {}: ".format(website))

                save_password(password, website)

            elif gen_question.lower() == 'y':
                generate_password(website)

            elif gen_question.lower() == 'exit':
                exit_program()

            else:
                time.sleep(1)
                print(colored('{} Enter Y or N.'.format(x_mark), 'red'))
                restart_program()


        pass
    elif beginProgram == "2":
        #look up a stored password
        pass

    elif beginProgram == "3":
        print(colored("Goodbye!", 'green'))
        pass

    elif beginProgram == "4":
        #first ask the user if they are sure they want to delete the database
        #prompt them for the password
        #delete the data
        pass
    
    else:
        time.sleep(1)
        print(colored('{} Enter one of the choices'.format(x_mark), 'red'))
        restart_program()

def restart_program():
    spinner = Halo(text=colored("Restarting program.", "red"), spinner=dots, color="red")
    spinner.start()
    time.sleep(1)
    spinner.stop()
    start()

def exit_program():
    spinner = Halo(text=colored("Exiting", "red"), spinner=dots, color="red")
    spinner.start()
    time.sleep(1)
    spinner.stop()
    print(colored("Goodbye!", "green"))

start()
		

		
		
"""

pip install termcolor
pip install halo

"""
