from phe import paillier
import re


# 123456789, (A23, 12,2), (B4, 32,1), (A2, 102), (CAA2, 34,5)

#([0-9]{9})\, (\([A-Z]{1,3}[0-9]{1,3}\, [0-9]+(\,[0-9]+)\))


# GERAÇÃO DE CHAVESs
public_key, private_key = paillier.generate_paillier_keypair()



# CIFRAGEM DOS DADOS
def complex(pub):
    print("Processo de cifragem dos dados...\n")
    fo = open('file.txt')
    f = fo.readlines()
    fo.close()
    cloud = {}
    arch = []
    for elem in f:
        id = elem.split(",",1)[0]
        raw = elem.split(",",1)[1]
        value = raw.split("),")
        for elem in value:
            elem = elem.replace("(","")
            elem = elem.replace(")","")
            acc = elem.split(",",1)[0].lstrip()
            data = elem.split(",",1)[1].replace(",",".")
            number = pub.encrypt(float(data)) #ciphered
            arch.append((acc,number))
        if id not in cloud.keys():
           cloud[id]=arch
        else:
            aux = cloud[id]
            cloud[id] = aux + arch
        arch = []

                
    print("Cifragem dos dados completa.\n")
    return cloud

# Cálculo da média
def avg(cloud,pk,value):
    tot = 0
    avg = 0

    for lista in cloud.values():
        
        for (k,elem) in lista:
            if k==value:
                avg += 1
                tot += elem
    if avg == 0:  
        return "Índice inexistente."

    tot = tot/avg
    return pk.decrypt(tot)

def main():
    x = complex(public_key)
    indice = input("Qual o índice de análise do qual pretende obter a média?\n")

    value = avg(x,private_key,indice)
    print(value)

main()
