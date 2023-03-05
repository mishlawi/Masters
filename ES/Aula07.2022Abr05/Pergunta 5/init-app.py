import sys
import json
from eVotUM.Cripto import eccblind

def printUsage():
    print("Usage:\npython init-app.py\npython init-app.py -init")

def parseArgs():
    if (len(sys.argv) == 1):
        main(1)
    if (len(sys.argv) > 1 and sys.argv[1] == "-init"):
        main(2)
    else:
        printUsage()

def main(k):
    initComponents, pRDashComponents = eccblind.initSigner()
    if (k==1):
        print("pRDashComponents: %s" % pRDashComponents)
    else:
        dic ={
            "pRDashComponents" : pRDashComponents,
            "initComponents" : initComponents
        }
        json_object = json.dumps(dic, indent = 4)
        with open("signer.json", "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    parseArgs()