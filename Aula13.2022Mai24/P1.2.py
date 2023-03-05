# Desenvolva um programa (na linguagem em que tiver mais experiência) que pede:

# + valor a pagar,
# + data de nascimento,
# + nome,
# + número de identificação fiscal (NIF),
# + número de identificação de cidadão (NIC),
# + numero de cartão de crédito, validade e CVC/CVV.

# Valide esse input de acordo com as regras de validação "responsável", apresentadas na aula teórica.


from datetime import date
import sys
import re


def getdigit(letter):
    if letter == '0':
        return 0
    elif letter == '1':
        return 1
    elif letter == '2':
        return 2
    elif letter == '3':
        return 3
    elif letter == '4':
        return 4
    elif letter == '5':
        return 5
    elif letter == '6':
        return 6
    elif letter == '7':
        return 7
    elif letter == '8':
        return 8
    elif letter == '9':
        return 9
    elif letter == 'A':
        return 10
    elif letter == 'B':
        return 11
    elif letter == 'C':
        return 12
    elif letter == 'D':
        return 13
    elif letter == 'E':
        return 14
    elif letter == 'F':
        return 15
    elif letter == 'G':
        return 16
    elif letter == 'H':
        return 17
    elif letter == 'I':
        return 18
    elif letter == 'J':
        return 19
    elif letter == 'K':
        return 20
    elif letter == 'L':
        return 21
    elif letter == 'M':
        return 22
    elif letter == 'N':
        return 23
    elif letter == 'O':
        return 24
    elif letter == 'P':
        return 25
    elif letter == 'Q':
        return 26
    elif letter == 'R':
        return 27
    elif letter == 'S':
        return 28
    elif letter == 'T':
        return 29
    elif letter == 'U':
        return 30
    elif letter == 'V':
        return 31
    elif letter == 'W':
        return 32
    elif letter == 'X':
        return 33
    elif letter == 'Y':
        return 34
    elif letter == 'Z':
        return 35

def validatecheckdigit(number):
    issecond = False
    soma = 0
    for dig in reversed(number):
        if issecond:
            dig *= 2;
            if dig > 9:
                dig -= 9
        soma += dig
        issecond = not issecond
    
    return (soma % 10) == 0

def printerror():
    print('wrong type of input, exiting')
    exit()

def validatevalue(value):
    # validar formato e tipo
    if re.fullmatch('(\d+([\.,]\d+)?)',value): 
        if ',' in value:
            value = value.replace(',','.')
        if '.' in value:
            value = float(value)
            # validar intervalo
            if value > sys.float_info.max:
                print('value too big, exiting')
                exit()
        else:
            value = int(value)
            # validar intervalo
            if value > sys.maxsize:
                print('value too big, exiting')
                exit()
    else:
        printerror()

def validatebirth(bd):
    # validar formato e tipo
    if re.fullmatch('\d\d/\d\d/\d\d\d\d',bd):
        d = int(bd.split('/')[0])
        m = int(bd.split('/')[1])
        y = int(bd.split('/')[2])
        # validar intervalo
        if y >= date.today().year - 135 and y <= date.today().year and m >= 1 and m <= 12 and d > 1:
            if (m in [1,3,5,7,8,10,12] and d <= 31) or (m in [4,6,9,11] and d <= 30) or (m == 2 and d <= 29):
                pass
        else:
            print('values out of range, exiting')
            exit()
    else:
        printerror()

def validatename(name):
    # validar formato e tipo
    if re.fullmatch('[a-zA-Z \u00C0-\u00FF]+',name):
        pass
    else:
        printerror()

def validatenif(nif):
    # validar formato e tipo
    if re.fullmatch('\d{9}',nif):
        nif = int(nif)
    else:
        printerror()

def validatenic(nic):
# validar formato e tipo
    if re.fullmatch('\d{8}',nic):
        cd = input("Check Digit: ")
        # validar formato e tipo do check digit
        if re.fullmatch('\d[A-Z\d][A-Z\d]\d',cd):
            d = []
            for c in nic:
                d.append(getdigit(c))
            for c in cd:
                d.append(getdigit(c))
            # validar número pelo check digit
            if validatecheckdigit(d):
                pass
            else:
                print('check digit was not validated, exiting')
                exit()
        else:
            printerror()
    else:
        printerror()

def validatecvc(cvc):
            # validar formato e tipo
            if re.fullmatch('\d{3,4}',cvc):
                pass
            else:
                printerror()

def validatevalidity(validity):
    # validar formato e tipo
    if re.fullmatch('(\d\d/\d\d)',validity):
        m = int(validity.split('/')[0])
        y = int(validity.split('/')[1])
        # validar intervalo
        if y >= int(str(date.today().year)[:2]) and m >= 1 and m <= 12:
            pass
        else:
            print('values out of range, exiting')
            exit()
    else:
        printerror()

def validatenumcard(numcard):
    # validar formato e tipo
    if re.fullmatch('(\d{13,16})',numcard):
        d = []
        for c in numcard:
            d.append(getdigit(c))
        # validar número pelo check digit
        if validatecheckdigit(d):
            pass
        else:
            printerror()

        validity = input("Validity: ")
        validatevalidity(validity)

        cvc = input("CVC/CVV: ")
        validatecvc(cvc)
    else:
        printerror()

# main

value = input("Value to pay: ")
validatevalue(value)

bd = input("Birth date (DD/MM/YYYY): ")
validatebirth(bd)

name = input("Name: ")
validatename(name)

nif = input("NIF (número de identificação fiscal): ")
validatenif(nif)

nic = input("NIC (número de identificação do cidadão): ")
validatenic(nic)

numcard = input("Credit card number: ")
validatenumcard(numcard)


print('All input is valid!')



