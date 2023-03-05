
import os
import json
import string
from getpass import getpass
from base64 import b64encode
from base64 import b64decode
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sympy import true

def derive_key(password):
    salt=b'z\x95\x81\x97,RrP\xde]4\x81\xe4\xf2\x91\x9c'
    key = PBKDF2HMAC(algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        ).derive(bytes(password,'utf-8'))
    return key


def auth(message,key):
        h = hmac.HMAC(key, hashes.SHA256())
        h.update(message)
        return h.finalize()


def verify(signature,key,message):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message)
    try:
        return h.verify(signature)
    except (InvalidSignature):
        print("Signature not verified")


def cipher(key,data):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), mode=modes.GCM(iv))
    encrypt = cipher.encryptor()
    ciphertext = encrypt.update(data) + encrypt.finalize()
    
    ct = b64encode(ciphertext).decode('utf-8')
    iv = b64encode(iv).decode('utf-8')
    signature = b64encode(auth(data, key)).decode('utf-8')
    tag = b64encode(encrypt.tag).decode('utf-8')

    result = json.dumps({'iv':iv, 'ciphertext':ct, 'signature':signature, 'tag':tag})
    
    return result


def decipher(key,data):
    try:
        b64 = json.loads(data)
        iv = b64decode(b64['iv'])
        ciphertext = b64decode(b64['ciphertext'])
        signature = b64decode(b64['signature'])
        tag = b64decode(b64['tag'])

        
        cipher = Cipher(algorithms.AES(key), mode=modes.GCM(iv,tag))
        decrypt = cipher.decryptor()
        plaintext = decrypt.update(ciphertext) + decrypt.finalize()
        try:
            verify(signature,key,plaintext)
        except (InvalidSignature):
            print("Signature not verified")
        return plaintext.decode("utf-8")
    except (ValueError, KeyError):
        print("Incorrect decryption")
    return ''


def validate_file(data):
    try: 
        b64 = json.loads(data)
        signature = b64decode(b64['signature'])
    except:
        return False
    if signature != None:
        return True
    else:
        return False

        

def menu():
    print("""
    ############### MENU ###############
    1 - Cipher file
    2 - Decipher file
    3 - Validate file
    0 - Leave
    Choose an option!
    """)




menu()
op = input()

while op != '0':
    if op not in string.digits:
        print("Unsupported character")
    elif int(op) == 1:
        file = input("Enter the file to cipher: ")
        password = getpass("Enter the password for the cipher key: ")
        fout = input("Enter a name for the output file: ")

        f = open(file,'rb')
        data = f.read()
        f.close()

        result = cipher(derive_key(password),data)
        
        f = open(fout,'w')
        f.write(result)
        f.close()

        print(f"\n\nDone! Check the {fout} file!")
    elif int(op) == 2:
        file = input("Enter the file to decipher: ")
        password = getpass("Enter the password for the cipher key: ")
        fout = input("Enter a name for the output file: ")

        f = open(file,'rb')
        data = f.read()
        f.close()

        result = decipher(derive_key(password),data)

        f = open(fout,'w')
        f.write(result)
        f.close()

        print(f"\n\nDone! Check the {fout} file!")
    elif int(op) == 3:
        file = input("Enter the file to validate: ")

        f = open(file,'rb')
        data = f.read()
        f.close()

        if validate_file(data):
            print("The file is valid")
        else:
            print("The file is not valid")

    menu()
    op = input()
        
