'''
O ChaCha20 é uma das duas cifras simétricas escolhidas para a encriptação dos novos protocolos de transporte,
nomeadamente o TLS 1.3 (cf. IETF RFC 8446), embora a sua utilização seja opcional.
Desenvolva em python (utilizando a biblioteca PyCryptodome) uma aplicação linha de comando que utilize o Chacha20 para cifrar um ficheiro,
em que o tamanho do nonce é de 12 bytes (conforme boas práticas definidas no IETF RFC RFC 7539).

No interface da linha de comando (CLI - command line interface) deve poder indicar a chave
(mas se o utilizador não a colocar, deve-lhe perguntar no inicio de execução do programa),
a operação a efetuar (cifra/decifra), ficheiro de input e ficheiro de output.

'''
import sys
import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes


def derive_key(password):
    salt=b'z\x95\x81\x97,RrP\xde]4\x81\xe4\xf2\x91\x9c'
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def cipher(key,data):
    nonce_rfc7539 = get_random_bytes(12)

    cipher = ChaCha20.new(key=key, nonce=nonce_rfc7539)
    ciphertext = cipher.encrypt(data)
    
    ct = b64encode(ciphertext).decode('utf-8')
    ciphertext = b64encode(ciphertext).decode('utf-8')
    nonce_rfc7539 = b64encode(nonce_rfc7539).decode('utf-8')

    result = json.dumps({'nonce':nonce_rfc7539, 'ciphertext':ct})
    
    return result


def decipher(key,data):
    try:
        b64 = json.loads(data)
        nonce = b64decode(b64['nonce'])
        ciphertext = b64decode(b64['ciphertext'])

        cipher = ChaCha20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
    except (ValueError, KeyError):
        print("Incorrect decryption")

    return plaintext.decode("utf-8")


# CLI

args = len(sys.argv)
if args>5 or args< 4:
    print("Not enough arguments")
else:
    if args < 5:
        # chacha.py encrypt/decrypt input.txt output.txt 
        while True:
            try:
                password = input("Please enter the key: ")
                cd = sys.argv[1]
                inputfile = sys.argv[2]
                outputfile = sys.argv[3]
            except ValueError:
                continue
            else:
                break
    if args == 5:
        # chacha.py encrypt/decrypt input.txt output.txt password
        cd = sys.argv[1]
        inputfile = str(sys.argv[2])
        outputfile = str(sys.argv[3])
        password = str(sys.argv[4])
    

    
    # managing input file and getting the data from it
    fin = open(inputfile)
    data = fin.read()
    fin.close()

    # managing output file and getting it ready to receive data  
    fout = open(outputfile,'w')

    # key derivation to get the 32 bytes for the chacha algorithm
    key = derive_key(password)

    if cd != "encrypt" and cd !="decrypt":
        print("unknown command: must spell correctly encrypt/decrypt !\n")
    else:
        if cd == "encrypt":
            print("encryption chosen")
            text = cipher(key,bytes(data, encoding='utf8'))
            print(text)
            fout.write(text)
            fout.close()
            
        if cd =="decrypt":
            print("decryption chosen")
            text = decipher(key,data)
            fout.write(text)
            print(text)
            fout.close()
    


