from inspect import signature
from eVotUM.Cripto import utils

import sys
import json
from eVotUM.Cripto import eccblind
from isort import file


def printUsage():
    print("Usage: verify-app.py -cert <certificado do assinante> -msg <mensagem original a assinar> -sDash <Signature> -f <ficheiro do requerente>")


def parseArgs():
    if (len(sys.argv) != 8):
        printUsage()
    else:
        eccPublicKeyPath = sys.argv[2]
        signature = sys.argv[6]
        data = sys.argv[4]
        file  = sys.argv[8]
        main(eccPublicKeyPath, data, signature, file)


def showResults(errorCode, validSignature):
    if (errorCode is None):
        if (validSignature):
            print("Valid signature")
        else:
            print("Invalid signature")
    elif (errorCode == 1):
        print("Error: it was not possible to retrieve the public key")
    elif (errorCode == 2):
        print("Error: pR components are invalid")
    elif (errorCode == 3):
        print("Error: blind components are invalid")
    elif (errorCode == 4):
        print("Error: invalid signature format")


def main(eccPublicKeyPath, data, signature, file):
    pemPublicKey = utils.readFile(eccPublicKeyPath)
    f = open(file, "r")
    content = json.load(f)
    blindComponents = content['blindComponents']
    pRComponents = content['pRComponents']
    f.close()

    errorCode, validSignature = eccblind.verifySignature(
        pemPublicKey, signature, blindComponents, pRComponents, data)
    showResults(errorCode, validSignature)


if __name__ == "__main__":
    parseArgs()
