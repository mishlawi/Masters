#!/usr/bin/python3 

from ast import arg, match_case
from cgitb import text
from enum import Flag
from nis import cat
from re import T
from gensim.models import Word2Vec
from re import *
import spacy
from googletrans import Translator
from prettytable import PrettyTable
import os
import sys
import getopt
from verbose import *
from functions import *


FLAGS = {
         '-g' : '',
         '-r' : '',
         '-t' : '',
         '--dir' : [],
         '--print' : False,
         '--spacy' : False,
         '--w2v' : False
        }


# pequeno-almoço | café da manhã -> refeiçao_PA
def getEquivalentes(frase):
    equivalentes = {}
    linhas = split(r"\n\r?",frase)
    x = 1
    for elem in linhas:
        if '//' in elem[0:2]:
            pass
        elif '->' in elem:
            aux = []
            values = split('->', elem)[0]
            aux.append(values.strip())
            
            key = split('->', elem)[1].strip()

            for k in aux:
                equivalentes[k] = key.strip()

        elif '()' in elem:
            nome = 'functions/' + elem[0:-2]+".py"
            if os.path.isfile(nome):
                equivalentes[elem] = "!!FUNCTION!!"
            else:
                print(f"A função {x} não existe. Não será considerada.")
        elif elem == "":
            pass
        else:
            print(f"A {x}a frase não está num formato correto. Não será considerada.")
        x += 1
        
    return equivalentes

# frase = '''
# pequeno almoço -> refeicao_PA
# acentos()
# words()
# '''


# getEquivalentes(frase)
def replacement(frase, regras):
    regras = getEquivalentes(regras)
    
    for regra in regras.keys():
        if regras[regra] == "!!FUNCTION!!":
            regra = regra[:-1] + 'frase)'
            frase = eval(regra)
        else:
            if regras[regra] == "":
                frase = sub(rf'{regra}', '', frase)
            else:  
                frase = sub(rf'\b{regra}\b', rf'__{regras[regra]}__', frase)
            
    frase = sub(r'__(.+?)__', r'\1', frase)
    return frase
        

def defineFunc(regras, f, commands):
    for regra in regras.keys():
        if regras[regra] == "!!FUNCTION!!":
            funcName = regra[:-2]
            path = 'functions/' + funcName + '.py'
            func = open(path, 'r')
            funcao = func.read()
            f.write(funcao + '\n')
            commands.append(rf"text = {funcName}(text)" + '\n')
        else:
            if regras[regra] == "":
                commands.append(rf"text = sub(r'{regra}', '', text)" + '\n')
            else:
                commands.append(rf"text = sub(r'\b{regra}\b', '__{regras[regra]}__', text)" + '\n')
    commands.append(r"text = sub(r'__(.+?)__', r'\1', text)" + '\n')

    return f, commands


def geraCodigo():
    f = open(FLAGS['-g'], "a", encoding="utf-8")
    commands = []
    commands.append("from re import * \n")
    commands.append("import sys\n\n")
    commands.append("text = open(sys.argv[1], 'r', encoding='utf-8').read()\n")

    if not FLAGS['-r'] == "":
        regras = getEquivalentes(FLAGS['-r'])
        f, commands = defineFunc(regras, f, commands)

    if not FLAGS['-t'] == "":
        commands.append(f"text = translate(text, '{FLAGS['-t']}')\n")
        func = open('functions/translate.py', 'r')
        funcao = func.read()
        f.write(funcao + '\n')
        func.close()

    if FLAGS['--spacy'] == True:    
        commands.append("text = spacy_func(text)\n")
        func = open(f'functions/spacy_func.py')
        funcao = func.read()
        f.write(funcao + '\n')
        func.close()
    elif FLAGS['--w2v'] == True:
        commands.append("text = w2v(text)\n")
        func = open(f'functions/w2v.py')
        funcao = func.read()
        f.write(funcao + '\n')
        func.close()

    for elem in commands:
        f.write(elem)
    f.write("print(text)\n")
    f.close()


def checkOpt(optlist, args):
    if len(optlist) == 0:
        perror()

    for elem in args:
        if elem[0] == '-':
            perror()

    if len(optlist) == 1 and len(args) == 0:
        if optlist[0][0] == '-V' or optlist[0][0] == '--version':
            printVersion()
        elif optlist[0][0] == "--help":
            printHelp()
        else:
            perror()
        exit(0)

    for elem in optlist:
        match elem[0]:
            case '-g':          # Gerar código python com as funcionalidades pedidas
                if elem[1] == '':
                    perror()
                if os.path.isfile(elem[1]):
                    os.remove(elem[1])
                FLAGS[elem[0]] = elem[1]
            case '-r':          # Leitura de um ficheiro de regras de reescrita
                if elem[1] == '':
                    perror_file('-r')
                if os.path.isfile(elem[1]):
                    f = open(elem[1], 'r', encoding='utf-8')
                    FLAGS[elem[0]] = f.read()
                    f.close()
                else:
                    perror_file(elem[1])
            case '-t':     # Tradução pt em it
                if match(r'\bIT|FR|ES|EN\b', elem[1], IGNORECASE):
                    FLAGS["-t"] = elem[1]
                else:
                    perror_flags('-t')
            case '--dir' :      # Executar ação a todos os ficheiros da mesma diretoria
                if elem[1] == '':
                    perror_file('--dir')
                if not os.path.isdir(elem[1]):
                    perror_dir(elem[1])
                listOfFiles = os.listdir(elem[1])
                for file in listOfFiles:
                    FLAGS[elem[0]].append(elem[1] + '/' + file)
            case '--print':
                FLAGS[elem[0]] = True
            case '--spacy':          # Utilização do spacy, palavra, lemma, ...
                FLAGS[elem[0]] = True
            case '--w2v':
                FLAGS[elem[0]] = True
    
    for elem in args:
        if os.path.isfile(elem):
            FLAGS['--dir'].append(elem)
        else:
            perror_file(elem)

    if FLAGS['--w2v'] == True and FLAGS['--spacy'] == True:
        perror_flags('--w2v')
        

def processa(text):
    if not FLAGS['-r'] == "":
        text = replacement(text, FLAGS['-r'])

    if not FLAGS['-t'] == "":
        text = translate(text,  FLAGS['-t'])

    if FLAGS['--spacy'] == True:
        text = spacy_func(text)

    elif FLAGS['--w2v'] == True:
        text = w2v(text)
    
    return text


def work():
    if not FLAGS['-g'] == "":
        geraCodigo()
    else:    
        for file in FLAGS['--dir']:
            textFile = open(file, "r", encoding="utf-8")
            newText = processa(textFile.read())
            textFile.close()
            if FLAGS['--print'] == False:
                file = split(r"\.", file)
                if len(file) == 2:
                    textFile = open(file[0] + "OUT." + file[1], "w", encoding="utf-8")
                else:
                    textFile = open(file[0] + "OUT", "w", encoding="utf-8")
                textFile.write(newText)
                textFile.close()
            else:
                print(newText)
                print("#@")


try:
    optlist, args = getopt.getopt(sys.argv[1:], 'g:r:t:V', ['dir=', 'help', 'print', 'spacy', 'version', 'w2v'])
except:
    perror()

checkOpt(optlist, args)
work()




