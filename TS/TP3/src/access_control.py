import sys, os
import os.path
from os import path
from pwd import getpwnam  
from pymongo import MongoClient
import configparser
import re

# Insere dados numa coleção
def insertData(file,user_name,email):
    config = configparser.ConfigParser()
    config.read(os.path.abspath('../config.ini'))
    user = config['Mongo']['user']
    password = config['Mongo']['password']
    client = MongoClient('mongodb://' + user + ':' + password + '@localhost:27017/fs') # Ligação mongo
    mydb = client.fs # DB do filesystem.
    if file not in mydb.list_collection_names():
        files = mydb[file]
    else:
        files = mydb.file
    
    file_data = {
        'uid': getpwnam(user_name).pw_uid,
        'email': email
    }

    result = files.insert_one(file_data)
    print('Inserted?',result.acknowledged)

# Validação
def validateAccess(filename,userName,email):
    if path.exists(filename): # Verifica se ficheiro existe.
        try:
            getpwnam(userName)
        except KeyError:
            print('User não existe no sistema.')
            sys.exit()
        if os.getuid() == os.stat(filename).st_uid: # Verifica se o user é dono do ficheiro
            if re.match('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}([.]\w{2,3})?$',email): # Verifica se email é válido
                return True
            else:
                print("Email inválido")
                sys.exit()
        else:
            print("Não és o owner do ficheiro")
            sys.exit()
    else:
        print("Ficheiro não existe")
        sys.exit()

def main():
    if(len(sys.argv)==4):
        if validateAccess(sys.argv[1],sys.argv[2],sys.argv[3]):
            insertData(sys.argv[1].split("/")[-1],sys.argv[2],sys.argv[3])
    else:
        print("Utilização: python3 access_control.py <caminho_ficheiro> <utilizador> <email>")

if __name__ == "__main__":
    main()
