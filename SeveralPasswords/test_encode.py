import os
import json
from Crypto.Cipher import AES
from os.path import isfile


def encrypt_data(data, master_pass):
    key = master_pass.encode('utf-8') #must be 16 bytes 
    cipher = AES.new(key, AES.MODE_EAX)
    the_nonce = cipher.nonce #A value that must never be reused for any other encryption done with this key (save alongside encrypted password?)
    print(the_nonce)
    nonce = the_nonce.decode(encoding='latin-1', errors="strict")
    print(nonce)

    if os.path.isfile("passwords.json"):
        try:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile["reddit"]["nonce"] = str(nonce)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
        except KeyError:
            with open('passwords.json', 'r') as jsondata:
                jfile = json.load(jsondata)
            jfile["reddit"] = {}
            jfile["reddit"]["nonce"] = str(nonce)
            with open('passwords.json', 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)

    else:
        jfile = {"reddit": {}}
        jfile["reddit"]["nonce"] = str(nonce)
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
            nonce = jfile["reddit"]["nonce"].encode('latin-1')
        except KeyError:
            pass

    key_encoded = key.encode('utf-8')
    cipher = AES.new(key_encoded, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_data)
    str_plaintext = plaintext.decode('utf-8')
    print(str_plaintext)

#encrypt_data('newTest', '1234567891234567')

decrypt_data("1234567891234567", b'\xeaj[\xe5\x1f\x84\xb1')