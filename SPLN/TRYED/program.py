from re import *
import sys


def dicionario(text):
    pass

def execute(text):
    pass

def substitute(line):
    pass

f = open(sys.argv[1], "r", encoding="utf-8").readlines()

for i in range(len(f)):
    line = f[i]
    if flag == True:
        if match(r"}", line):
            flag = False
        continue
    line = split("->", line)
    if len(line) > 1:
        substitute(line)
        flag = True
    line = split("=>", line)
    if len(line) > 1:
        execute(f[i:])
        if match(r"{", line):
            flag = True
    line = split("=", line)
    if len(line) > 1:
        dicionario(f[i:])
    