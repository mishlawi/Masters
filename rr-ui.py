#!/usr/bin/python3 


from pydoc import doc
import re
import json
import textwrap
import os
from webbrowser import get
from rr import translate, spacyWorking
from verbose import *

def menu():
        
    return input(textwrap.dedent('''
                1 - Ativar a flag para gerar código python
                2 - Utilizar regras NL-flex
                3 - Traduzir
                4 - Inserir ficheiros ou diretorias de ficheiros
                5 - Ativar a flag de print
                6 - Ativar a flag de spacy
                7 - Ativar a flag de w2v
                8 - Correr o programa
                9 - Ajuda
                10 - Versão
                0 - Sair
                ''')) # what more to add????

def showDocs(documentos):
    
    if len(documentos.keys())>0:
        
        x = textwrap.dedent(f'''
        Documentos Existentes:

        ''')
        v=0
        for elem in documentos.keys():
            x+=textwrap.dedent(f'''{v}. {elem}
            ''')
            v+=1
    else:
        x=''
        
    return x

def docQuestion():
    
    return int(input(textwrap.dedent('''
            Documento já foi carregado?
            1- Yes
            2- No
            0- Leave
            ''')))

 
def interface(documentos):
    
    print(showDocs(documentos))
    
    op = int(menu())

    if op==0:
        print("\n\nDesenvolvido por Tiago Barata, Angélica Cunha, Duarte Vilar SPLN-2022")
        return

    elif op==1:
        
        v = docQuestion()

        if v==1 and len(documentos)>0:
        
            os.system('cls||clear')
            print("Escolha o documento a utilizar")
        
            used = int(input(showDocs(documentos)))
            if used>len(documentos):
                print("Indice superior ao numero de documentos existentes\n")

            else:
                document = list(documentos.keys())[used]
                
                try:
                    f = open(document,"r")
                    print("Okay, tudo certo.")
                
                except FileNotFoundError:
                    print("Algum erro acontenceu...")
                
                os.system('cls||clear')                                            
                eq = input("\nAtenção, ao definir equivalências multi-word essas alterações serão atribuídas ao documento:\n")
                
                equivalencias = getEquivalentes(eq)
                texto = f.read()
                f.close()
                for elem in equivalencias.keys():
                    texto = re.sub(str(elem),str(equivalencias[elem]),texto)

                f = open(document,'w')
                ## update equivalencias que foram agora criadas
                
                value = documentos[document]['equivalencias']
                value.update(equivalencias)
                documentos[document]['equivalencias'] = value

                # update do json

                json_obj = json.dumps(documentos, indent = 4)
                
                with open("documentos.json", "w") as outfile:
                    outfile.write(json_obj)
                
                outfile.close()    

                # update texto
                f.write(texto)
                f.close()
                print("Done\n")
            
            interface(documentos)

        elif v==1 and len(documentos)==0:
            os.system('cls||clear')
            print("Não existem documentos carregados!\n")
            interface(documentos)
        
        elif v==2:

            os.system('cls||clear')
            newDoc = input("Nome do documento a ser considerado:\n")
            
            try:
                if newDoc in documentos.keys():
                    print("Esse documento já foi carregado")
                    exit
                    interface(documentos)
                    return
                else:
                    f = open(newDoc,"r")
                    print("existe")
            
            except FileNotFoundError:
                os.system('cls||clear')
                print("Ficheiro não existe.\n")
                exit
                interface(documentos)
                return

            eq = input("\nAtenção, ao definir equivalências multi word, essas alterações serão atribuídas ao documento:\n")

            equivalencias = getEquivalentes(eq)
            print("Feito, documento adicionado aos registos")
            # update documentos
            documentos[newDoc] = {'equivalencias':equivalencias,'accoes':{}}
            
            # Serializing json and writing json in proper doc # 
            json_obj = json.dumps(documentos, indent = 4)
            
            with open("documentos.json", "w") as outfile:
                outfile.write(json_obj)
            outfile.close()

            texto = f.read()
            
            f.close()
            f = open(newDoc,'w')

            for elem in equivalencias.keys():
                texto = re.sub(elem,equivalencias[elem],texto)
            
            f.write(texto)
            f.close()
            interface(documentos)
        
        elif v==0:
            exit
            os.system('cls||clear')
            interface(documentos)
        else:
            print("Opção errada!")              


    elif op==2:
        
        v = docQuestion()
        
        if v==1 and len(documentos)>0:
            
            os.system('cls||clear')
            print("Escolha o documento a utilizar")
        
            used = int(input(showDocs(documentos)))
            if used>len(documentos):
                print("Indice superior ao numero de documentos existentes\n")

            else:
                document = list(documentos.keys())[used]
                
                try:
                    f = open(document,"r")
                    print("Okay, tudo certo.")
                
                except FileNotFoundError:
                    print("Algum erro acontenceu...")
                
                os.system('cls||clear')              

            accao = input("A ação de relação que definir torna-se permanente no documento escolhido.\n")
            
        
        elif v==1 and len(documentos)==0:
            os.system('cls||clear')
            print("Não existem documentos carregados!\n")
            interface(documentos)
        
        elif v==2:
            print("alskgalsgk")
    
        #existe

        interface(documentos)
    
    elif op==3:

        print("3")
        os.system('cls||clear')
        
        if len(documentos.keys())>0:
            
            print("Escolha o documento a verificar o historial de equivalencias feitas")
                
            used = int(input(showDocs(documentos)))
            
            if used>len(documentos):
            
                print("Indice superior ao número de documentos existentes\n")
            
            else:
                document = list(documentos.keys())[used]
                f = open("documentos.json", "r")
                dic = json.load(f)
                x = 0
                os.system('cls||clear')
                
                for key,value in zip(dic[document]['equivalencias'].keys(),dic[document]['equivalencias'].values()):
                    print(textwrap.dedent(f'''{x}. {key}   ->   {value}'''))
                    x+=1
                
                f.close()        
        else:
            print("Sem dados disponíveis")
        
        interface(documentos)
        
        
    elif op==4:
        print("4")
        interface(documentos)
    
    elif op==5:
        
        if v==1 and len(documentos)>0:
            
            os.system('cls||clear')
            print("Escolha o documento a utilizar")
        
            used = int(input(showDocs(documentos)))
            if used > len(documentos):
                print("Indice superior ao número de documentos existentes\n")
            else:

                document = list(documentos.keys())[used]
                
                try:
                    f = open(document,"r")
                    print("Okay, tudo certo.")
                
                except FileNotFoundError:
                    print("Algum erro acontenceu...")
                

                os.system('cls||clear')
                

        elif v==1 and len(documentos)==0:
            os.system('cls||clear')
            print("Não existem documentos carregados!\n")
            interface(documentos)
        
        elif v==2:

            os.system('cls||clear')
            newDoc = input("Nome do documento a ser considerado:\n")
            
            try:
                if newDoc in documentos.keys():
                    print("Esse documento já foi carregado")
                    return
                else:
                    f = open(newDoc,"r")
                    texto = f.read()

                    #### spacy

                    spacyWorking(texto)
                    print("existe\n")
            
            except FileNotFoundError:
                exit
                os.system('cls||clear')
                print("Ficheiro não existe.\n")
                return
            
            interface(documentos)
    elif op==6:
        
        v = int(input(textwrap.dedent('''
            1- Documento carregado
            2- Documento por carregar
            3 - Escrita livre
            0- Leave
            ''')))

        if v==1 and len(documentos)>0:
            
            os.system('cls||clear')
            print("Escolha o documento a utilizar")
        
            used = int(input(showDocs(documentos)))
            if used > len(showDocs(documentos)):
                print("Indice superior ao numero de documentos existentes\n")
            document = list(documentos.keys())[used]
            
            try:
                f = open(document,"r+")
                print("Okay, tudo certo.")
            
            except FileNotFoundError:
                print("Algum erro acontenceu...")
                return
            
            texto = f.read()
            translate(texto)
        
        
        elif v==1 and len(documentos)==0:
            os.system('cls||clear')
            print("Não existem documentos carregados!\n")
            interface(documentos)
        
        elif v==2:
            
            os.system('cls||clear')
            newDoc = input("Nome do documento a ser considerado:\n")
            
            try:
                if newDoc in documentos.keys():
                    print("Esse documento já foi carregado")
                    exit
                    interface(documentos)
                    return
                else:
                    f = open(newDoc,"r+")
                    print("existe")
            
            except FileNotFoundError:
                os.system('cls||clear')
                print("Ficheiro não existe.\n")
                exit
                interface(documentos)
                return
            texto = f.read()
            translate(texto)

            f.close()
        elif v==3:
            os.system('cls||clear')
            texto = input("Insira o texto que pretende ver analisado pelo bot\n")
            translate(texto)

        interface(documentos)
    
    else:
        print("Opção errada!!!")
        os.system('cls||clear')
        interface(documentos)



def main():
    documentos= {}
    try:
        f = open('.documentos.json')
        documentos = json.load(f) 
        interface(documentos)
    
    except FileNotFoundError:
        interface({})
    
main()
    

