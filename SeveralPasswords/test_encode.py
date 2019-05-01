import os
import json
from Crypto.Cipher import AES
from os.path import isfile


def encrypt_data(data, master_pass, website):
    final_master = master_pass + '================'
    key = final_master[:16].encode('utf-8') #must be 16 bytes 

    cipher = AES.new(key, AES.MODE_EAX)
    the_nonce = cipher.nonce #A value that must never be reused for any other encryption done with this key (save alongside encrypted password?)
    print(the_nonce)
    nonce = the_nonce.decode(encoding='latin-1', errors="strict")
    print(nonce)




    data_to_encrypt = data.encode('utf-8') #password that would be encrypted where *data* is the password
    ciphertext = cipher.encrypt(data_to_encrypt)
    print(ciphertext)
    ciphertext_decoded = ciphertext.decode(encoding='latin-1', errors="strict")
    print(ciphertext_decoded)
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

#encrypt_data('testGoogle', 'master_key')

#decrypt_data('master_key', 'reddit')