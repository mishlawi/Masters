import os
from cryptography.hazmat.primitives import hashes, hmac 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Emitter:
  def __init__(self, password):
      self.cipher_key = None
      self.mac_key = None
      self.password = password
      self.key_salt = os.urandom(16)
      
  def derivate_key(self):
      kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.key_salt,iterations=390000,)
      self.mac_key = kdf.derive(self.password)
    
  
      