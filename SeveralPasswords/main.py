"""

pip install termcolor
pip install halo
pip install pycryptodome

"""

import random
import time
import os
import json

from halo import Halo
from os.path import isfile
from termcolor import colored
from Crypto.Cipher import AES


alphabetLower = "abcdefghijklmnopqrstuvwxyz"
alphabetUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specialChar = "!@#$%^&*()-_"

checkmark = "\u2713"
x_mark = "\u2717"

dots = {"interval": 80, "frames": ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]}

def encrypt_data(data, master_pass, website):
    final_master = master_pass + '================' #concatenated extra characters in the case that the password is less than 16 characters
    key = final_master[:16].encode('utf-8') #must be 16 bytes 

    cipher = AES.new(key, AES.MODE_EAX)
    the_nonce = cipher.nonce #A value that must never be reused for any other encryption done with this key (save alongside encrypted password?)
    nonce = the_nonce.decode(encoding='latin-1', errors="strict") #encoded in order to be able to write it to the json file. 

    data_to_encrypt = data.encode('utf-8') #password that would be encrypted where *data* is the password
    ciphertext = cipher.encrypt(data_to_encrypt)
    ciphertext_decoded = ciphertext.decode(encoding='latin-1', errors="strict")
    if os.path.isfile("passwords.json"):
        try:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile[website]["nonce"] = str(nonce)
            jfile[website]["data"] = str(ciphertext_decoded)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
        except KeyError:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile[website] = {}
            jfile[website]["nonce"] = str(nonce)
            jfile[website]["data"] = str(ciphertext_decoded)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)

    else:
        jfile = {website: {}}
        jfile[website]["nonce"] = str(nonce)
        jfile[website]["data"] = str(ciphertext_decoded)
        with open('passwords.json', 'w') as jsondata:
            json.dump(jfile, jsondata, sort_keys=True, indent=4)

def decrypt_data(key, website):

    if os.path.isfile('passwords.json'):
        try:
            with open('passwords.json', 'r') as jdata:
                jfile = json.load(jdata)
            nonce = jfile[website]["nonce"].encode('latin-1')
            data = jfile[website]["data"].encode('latin-1')
        except KeyError:
            pass


    formatted_key = key + '================'
    key_encoded = formatted_key[:16].encode('utf-8')
    cipher = AES.new(key_encoded, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(data)
    str_plaintext = plaintext.decode('utf-8')
    print(str_plaintext)

def generate_password(website):
    password = []

    length = input("How many characters do you want your password to be? (At least 8) ")
  
    if int(length) < 8:
        print(colored("{} A password of at least 8 characters is required".format(x_mark), "red"))
        restart_program()
    
    elif length.lower() == 'exit':
        exit_program()
    
    else:
        for i in range(0, int(length)):
            password.append(random.choice(random.choice([alphabetLower, alphabetUpper, digits, specialChar]))) 
    
        finalPass = "".join(password)

        spinner = Halo(text=colored("Generating Password", "green"), spinner=dots, color="green")
        spinner.start()
        time.sleep(1)
        spinner.stop()

        print(colored(finalPass, "yellow"))
        loop = input("Generate a new password? (Y/N) ")

        if loop.lower() == "y":
            generate_password(website)

        elif loop.lower() == 'exit':
            exit_program()

        elif loop.lower() == 'n':
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

                else: #initialize the file in case it doesn't exist off the start.
                    jfile = {website: {}}
                    jfile[website]["password"] = finalPass
                    with open('passwords.json', 'w') as jsondata:
                        json.dump(jfile, jsondata, sort_keys=True, indent=4)




                time.sleep(1)
                spinner.stop()
                print(colored("{} Saved successfully. Thank you!".format(checkmark), "green"))
            elif savePass.lower() == 'n' or 'exit':
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

    else: #initialize the file in case it doesn't exist off the start.
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
    print(colored("\nENTER 'exit' AT ANY POINT TO EXIT\n", "magenta"))
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

                time.sleep(1)
                loop_program()

            elif gen_question.lower() == 'y':
                generate_password(website)
                time.sleep(1)
                loop_program()

            elif gen_question.lower() == 'exit':
                exit_program()

            else:
                time.sleep(1)
                print(colored('{} Enter Y or N.'.format(x_mark), 'red'))
                restart_program()


        pass
    elif beginProgram == "2": #look up a stored password
        #Load the passwords stored with a bit of flair
        if os.path.isfile('passwords.json'): #but first we have to check if the file exists
            print(colored("Current Passwords Stored:", "yellow"))
            with open("passwords.json", 'r') as jsondata:
                pass_list=json.load(jsondata)
            spinner = Halo(text=colored("Loading Passwords", "yellow"), color="yellow", spinner=dots)
            spinner.start()
            time.sleep(2)
            spinner.stop()
            for i in pass_list:
                print(colored("--{}".format(i), "yellow"))

            website = input("Enter the website for the password you want to retrieve: ")

            if website.lower() == 'exit':
                exit_program()
            
            elif website == '':
                print(colored("No website name given.", "red"))
                restart_program()
            else:
                try:
                    with open('passwords.json', 'r') as jsondata:
                            jfile = json.load(jsondata)
                    user_password = jfile[website]["password"]

                    print(colored("Your password is: {}".format(user_password), "yellow"))
                    loop_program()
                except KeyError:
                    print(colored("{} Password not found for {} . Create a password for it or enter a new name.".format(x_mark, website), "red"))
                    restart_program()
        else:
            print(colored("{} Password File Does Not Exist. Restart the program and go through option 1 to initialize.".format(x_mark), "red"))
            restart_program()




    elif beginProgram == "3":
        print(colored("Goodbye!", 'green'))

    elif beginProgram == "4":
        #first ask the user if they are sure they want to delete the database
        print(colored("{} ARE YOU SURE YOU WANT TO DELETE YOUR DATA {}".format(x_mark, x_mark), "red"))
        choice = input("(Y/N): ")


        if choice.lower() == "y": #delete the data
            if os.path.isfile("passwords.json"):
                spinner = Halo(text=colored("Deleting all password data.", "red"), color="red", spinner=dots)
                spinner.start()
                time.sleep(1)
                spinner.stop()
                with open('passwords.json', 'r') as jsondata:
                    jfile = json.load(jsondata)
                jfile = {}
                with open('passwords.json', 'w') as jsondata:
                    json.dump(jfile, jsondata, sort_keys=True, indent=4)
                print(colored("{} Password data deleted successfully.".format(checkmark), "green"))
            else:
                print(colored("{} Password File Does Not Exist. Restart the program and go through option 1 to initialize.".format(x_mark), "red"))
                restart_program()

    elif beginProgram.lower() == 'exit':
        exit_program()
    
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

def loop_program():
    option = input("Would you like to return to the beginning? (Y/N) ")
    if option.lower() == 'y':
        restart_program()
    elif option.lower() == 'n' or 'exit':
        exit_program()
    else:
        print(colored("Invalid option.", "red"))
        exit_program()

		


		
start() #here we go :)
		
