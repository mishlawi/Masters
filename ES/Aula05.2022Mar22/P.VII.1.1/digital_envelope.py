
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20
from base64 import b64decode
from base64 import b64encode
import os
import json
import sys


def pkfile_pw(password):
    salt = b'W\x8e\xeaP7@\x96M?\xf0Q\xabN\xceK\xcf'
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def session_keygen():
    password = get_random_bytes(16)
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def elliptic_keygen():
    private_key = ec.generate_private_key(ec.SECP256R1)
    public_key = private_key.public_key()
    return private_key, public_key


def elliptic_keygen(private_file, public_file, password):
    private_key = ec.generate_private_key(ec.SECP256R1)
    public_key = private_key.public_key()
    f = open(f'{private_file}.pem', 'wt')
    serialized_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password=pkfile_pw(password)))
    f.write(serialized_private.decode("utf-8"))
    f.close()

    f = open(f'{public_file}.pem', 'wt')
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    f.write(serialized_public.decode("utf-8"))
    f.close()


def cipher(receiver_public_key, private_key, session_key, data):
    nonce_rfc7539 = get_random_bytes(12)
    cipher_text = ChaCha20.new(key=session_key, nonce=nonce_rfc7539)
    ciphertext = cipher_text.encrypt(data)

    shared_key = private_key.exchange(ec.ECDH(), receiver_public_key)

    nonce = os.urandom(12)
    cipher = ChaCha20.new(key=shared_key, nonce=nonce)
    ciphersessionkey = cipher.encrypt(session_key)

    ct = b64encode(ciphertext).decode('utf-8')
    nonce_rfc7539 = b64encode(nonce_rfc7539).decode('utf-8')
    csk = b64encode(ciphersessionkey).decode('utf-8')
    nonce_encoded = b64encode(nonce).decode('utf-8')

    result = json.dumps({'nonce': nonce_rfc7539, 'ciphertext': ct})
    result_csk = json.dumps({'nonce': nonce_encoded, 'ciphersession': csk})

    return result_csk, result


def decipher(key_file, password, sender_key_file, csk, data):

    f = open(key_file, 'rb')
    private_key = serialization.load_pem_private_key(
        f.read(), password=pkfile_pw(password), )
    f.close()

    f = open(sender_key_file, 'rb')
    receiver_public_key = serialization.load_pem_public_key(f.read(), )
    f.close

    b64_session = json.loads(csk)
    nonce_session = b64decode(b64_session['nonce'])
    ciphersession = b64decode(b64_session['ciphersession'])

    b64 = json.loads(data)
    nonce = b64decode(b64['nonce'])
    ciphertext = b64decode(b64['ciphertext'])

    shared_key = private_key.exchange(ec.ECDH(), receiver_public_key)

    cipher = ChaCha20.new(key=shared_key, nonce=nonce_session)
    session_key = cipher.decrypt(ciphersession)

    cipher = ChaCha20.new(key=session_key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext.decode("utf-8")

######################################################


args = len(sys.argv)
if args > 4:
    if sys.argv[1] == 'generate_keys':
        # chacha.py generate_keys public_key_file private_key_file password
        public_file = str(sys.argv[2])
        private_file = str(sys.argv[3])
        password = str(sys.argv[4])
        elliptic_keygen(private_file, public_file, password)
        print("keys generated! check the files")
    elif sys.argv[1] == 'encrypt':
        # chacha.py encrypt key_file input.txt output.txt

        if args == 5:
            key_file = sys.argv[2]
            inputfile = sys.argv[3]
            outputfile = sys.argv[4]

            private, public = elliptic_keygen()

            fin = open(inputfile)
            data = fin.read()
            fin.close()

            f = open(key_file, 'rt')
            receiver_public_key = serialization.load_pem_public_key(f.read(), )
            f.close

            print("encryption chosen")
            session_key = session_keygen()

            session, text = cipher(
                receiver_public_key, private, session_key, bytes(data, encoding='utf8'))
        elif args == 8:
            # chacha.py encrypt key_file input.txt output.txt public_key_file private_key_file password
            key_file = sys.argv[2]
            inputfile = sys.argv[3]
            outputfile = sys.argv[4]
            public_file = str(sys.argv[5])
            private_file = str(sys.argv[6])
            password = str(sys.argv[7])
            elliptic_keygen(private_file, public_file, password)

            fin = open(inputfile)
            data = fin.read()
            fin.close()

            fpub = open(key_file, 'rb')
            receiver_public_key = serialization.load_pem_public_key(
                fpub.read(), )
            fpub.close

            fpriv = open(f'{private_file}.pem', 'rb')
            private = serialization.load_pem_private_key(
                fpriv.read(), password=pkfile_pw(password), )
            fpriv.close

            print("encryption chosen")
            session_key = session_keygen()

            session, text = cipher(
                receiver_public_key, private, session_key, bytes(data, encoding='utf8'))

        fout = open('session_key.txt', 'w')
        fout.write(session)
        fout.close()
        fout = open(outputfile, 'w')
        fout.write(text)
        fout.close()
        print(f"done! check the file {outputfile}")

    elif sys.argv[1] == 'decrypt':
        # chacha.py decrypt key_file password pub_key session_key.txt input.txt output.txt
        priv_key_file = sys.argv[2]
        password = sys.argv[3]
        pub_key = sys.argv[4]
        session_file = sys.argv[5]
        inputfile = sys.argv[6]
        outputfile = sys.argv[7]

        fin = open(inputfile)
        data = fin.read()
        fin.close()

        fsession = open(session_file)
        csk = fsession.read()
        fsession.close()

        print("decryption chosen")
        text = decipher(priv_key_file, password, pub_key, csk, data)
        fout = open(outputfile, 'w')
        fout.write(text)
        fout.close()
        print(f"done! check the file {outputfile}")
    else:
        print("unknown command! please use 'generate_keys', 'encrypt' or 'decrypt'")
else:
    print("wrong number of arguments!")
