from cryptography.hazmat.primitives import hashes, hmac 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KEY_DIGEST_LEN = 32 # Bytes
NONCE_LEN = 12 # Bytes
SALT_LEN = 16 # Bytes

class Receiver:
    def __init__(self, password):
      self.key = None
      self.password = password
    
    def derivate_key(self, dados):
        pass
    
        