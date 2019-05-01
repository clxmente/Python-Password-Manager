from hashlib import sha256

def hex_digest(password):
    print(sha256(password).hexdigest())

hex_digest("test".encode('utf-8'))