import os
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hmac
import hashlib

class Emitter:
    def __init__(self):
        self.cipher_key = None
        self.mac_key = None
        self.key_salt = os.urandom(16)
        self.nonce = 0
        self.metadata = 0
      
    def derivate_key(self):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.key_salt,iterations=390000,)
        self.mac_key = kdf.derive(b'my great password')

    def send_message(self, message):
        message = message.encode('utf-8')
        h = hmac.new(self.mac_key, message, hashlib.sha256)
        digest = h.digest()
        metadata = self.key_salt

        nonce = os.urandom(12)
        metadata += nonce
        aesgcm = AESGCM(self.mac_key)
        ct = aesgcm.encrypt(nonce, message, metadata)

        return digest + nonce + self.key_salt + ct

em = Emitter()
em.derivate_key()
#print(str(em.send_message('oiiiiiii'),('utf-8')))




  
      