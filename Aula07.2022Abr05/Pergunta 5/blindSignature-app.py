from eVotUM.Cripto import utils

import sys
import json
from eVotUM.Cripto import eccblind

def printUsage():
    print("Usage: blindSignature-app.py -key <chave privada> -bmsg <Blind message>")

def parseArgs():
    if (len(sys.argv) != 5):
        printUsage()
    else:
        privatekey = sys.argv[2]
        bmsg = sys.argv[4]
        main(privatekey, bmsg)

def showResults(errorCode, blindSignature):
    if (errorCode is None):
        print("Blind signature: %s" % blindSignature)
    elif (errorCode == 1):
        print("Error: it was not possible to retrieve the private key")
    elif (errorCode == 2):
        print("Error: init components are invalid")
    elif (errorCode == 3):
        print("Error: invalid blind message format")

def main(privatekey, bmsg):
    f = open('signer.json')
    data = json.load(f)
    passphrase = input("Passphrase: ")
    initComponents = data['initComponents']
    f.close()
    errorCode, blindSignature = eccblind.generateBlindSignature(privatekey, passphrase, bmsg, initComponents)
    showResults(errorCode, blindSignature)

if __name__ == "__main__":
    parseArgs()
