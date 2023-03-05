import sys
import json
from eVotUM.Cripto import eccblind


def printUsage():
    print("Usage: desofusca-app.py -s <Blind Signature> -RDash <pRDashComponents>")

def parseArgs():
    if (len(sys.argv) != 5):
        printUsage()
    else:
        bsign = sys.argv[2]
        prDash = sys.argv[4]
        main(bsign, prDash)

def showResults(errorCode, signature):
    if (errorCode is None):
        print("Signature: %s" % signature)
    elif (errorCode == 1):
        print("Error: pRDash components are invalid")
    elif (errorCode == 2):
        print("Error: blind components are invalid")
    elif (errorCode == 3):
        print("Error: invalid blind signature format")

def main(bsign, prDash):
    f = open('applicant.json')
    data = json.load(f)
    blindComponents = data['blindComponents']
    f.close()
    errorCode, signature = eccblind.unblindSignature(bsign, prDash, blindComponents)
    showResults(errorCode, signature)

if __name__ == "__main__":
    parseArgs()
