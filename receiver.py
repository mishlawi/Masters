from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hmac
import hashlib

KEY_DIGEST_LEN = 32 # Bytes
NONCE_LEN = 12 # Bytes
SALT_LEN = 16 # Bytes

class Receiver:
    def __init__(self):
      self.key = None
    
    def derivate_key(self, dados):
      salt = self.unpack_data(dados)[-2]
      kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,)
      self.key = kdf.derive(b'my great password')
    
    def unpack_data(self, dados):
      # dados : key_digest + nonce + salt + mensagem
      # 0 - 31 : key_digest (32 bytes)
      # 32 - 43 : nonce para decode (12 bytes)
      # 44 - 59 : salt para derivar chave (16 bytes)
      # 60 ... : texto cifrado
      key_digest = dados[:KEY_DIGEST_LEN]
      nonce = dados[KEY_DIGEST_LEN:KEY_DIGEST_LEN + NONCE_LEN]
      salt = dados[KEY_DIGEST_LEN + NONCE_LEN:KEY_DIGEST_LEN + NONCE_LEN + SALT_LEN]
      ct = dados[KEY_DIGEST_LEN + NONCE_LEN + SALT_LEN:]
      
      return key_digest, ct, salt, nonce
    
    def read_message(self, ct):
      key_digest, ct, salt, nonce = self.unpack_data(ct)
      h = hmac.new(self.key, None, hashlib.sha256)
      # gera digest para a mensagem
      h.update(ct)
      new_digest = h.digest()
      try :
          # verifica se o digest gerado acima é igual ao digest recebido como parâmetro
          new_digest == key_digest
      except:
        raise Exception("Falha na autenticidade da chave") 
        
      metadata = salt + nonce 

      aesgcm = AESGCM(self.key)
      try:
          texto_limpo = aesgcm.decrypt(nonce, ct, metadata)
      except cryptography.exceptions.InvalidTag:
          # Falha na verificação da autenticidade 
          error_code, texto_limpo = 1, None
      error_code, texto_limpo = None, texto_limpo.decode('utf-8')

      self.show_results(error_code,texto_limpo)
    
    def show_results(self, error, message):
        if error == None:
            print("Texto decifrado: %s" %message)
        elif error == 1:
            print("Falha na verificação da autenticidade.")



