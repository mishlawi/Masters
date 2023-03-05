import sys
import json
from eVotUM.Cripto import eccblind

def printUsage():
    print("ofusca-app.py -msg <mensagem a assinar> -RDash <pRDashComponents>")

def parseArgs():
    if (len(sys.argv) != 5):
        printUsage()
    else:
        msg = sys.argv[2]
        pRDash = sys.argv[4]
        main(msg, pRDash)

def showResults(errorCode, result):
    if (errorCode is None):
        blindComponents, pRComponents, blindM = result
        print("Blind message: %s" % blindM)
        dic ={
            "blindComponents" : blindComponents,
            "pRComponents" : pRComponents
        }
        json_object = json.dumps(dic, indent = 4)
        with open("applicant.json", "w") as outfile:
            outfile.write(json_object)
    elif (errorCode == 1):
        print("Error: pRDash components are invalid")

def main(msg, pRDash):
    errorCode, result = eccblind.blindData(pRDash, msg)
    showResults(errorCode, result)

if __name__ == "__main__":
    parseArgs()
