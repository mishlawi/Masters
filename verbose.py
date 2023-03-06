# Print the help option
def printHelp():
    print("\t\t\t\t\t\t\t\tUser Commands")
    print("\t\tWelcome to rr, the filter of rewriting system of natural language")
    print("NAME")
    print("\t\rr - make your text analisys simple and pre-process for others tools")
    print("SINOPSE")
    print("\t\trr [OPTIONS...] [FILE...]")
    print("DESCRIPTION")
    print("\t\trr have a lot of tools, and the central focus is make easy the work with natural language in computer science.")
    print("OPTIONS")
    print("\tGeneric Program Information")
    print("\t\t--help Output a usage message and exit.")
    print()
    print("\t\t-V, --version.")
    print("\t\t\t\tOutput the version number of highlight and exit.")
    print("\tGeneral Output Control")
    print()
    print("\t\t--dir <path>")
    print("\t\t\t\tAplies the filter of all content of some specific directory.")
    print()
    print("\t\t-g <file-name>.py")
    print("\t\t\t\tSupress normal output; instead change files, creating a OUTPUT file, generated a python filter with specified functions.")
    print()
    print("\t\t-r <rules-file>")
    print("\t\t\t\tTakes a rules file written in NL-flex (not all commands), and use that rules to make changes to file.")
    print()
    print("\t\t-t <LANG>")
    print("\t\t\t\tTranslate file in specific <LANG>.")
    print("\t\t\t\tSource language supported: PT.")
    print("\t\t\t\tDestiny specified <LANG>: EN, ES, FR, IT.")
    print()
    print("\t\t--print")
    print("\t\t\t\tSupress normal output; instead change files, creating a OUTPUT file, print the result on screen. If more that one files is in use, they will separeted with a line with '#@'.")
    print()
    print("\t\t--spacy")
    print("\t\t\t\tUses spacy to create a OUTPUT file with ocurrence_phase_occurence, word, word_lemma and POS.")
    print()
    print("\t\t--w2v")
    print("\t\t\t\tPreprosses files to using in word embendings, creating a list of list of words, without stopwords and union of multi-word terms.")
    print()
    print("UTILS")
    print("\tImplemented functions to call in <rules-file>")
    print("\t\tacentos()")
    print("\t\t\t\tRemoves accents from all words.")
    print()
    print("\t\tconverter2digit()")
    print("\t\t\t\tSubstitute words referer numbers in digit number.")
    print()
    print("\t\tconverter2digit()")
    print("\t\t\t\tSubstitute digit number in words referer numbers.")
    print()
    print("\t\temoji2text()")
    print("\t\t\t\tSubstitute emoji for ':meaning:'.")
    print()
    print("\t\tlower()")
    print("\t\t\t\tAll words in small case.")
    print()
    print("\t\tspacy_func()")
    print("\t\t\t\tThe same as flag '--spacy'.")
    print()
    print("\t\ttext2emoji()")
    print("\t\t\t\tSubstitute ':meaning:' by emoji.")
    print()
    print("\t\ttranslate()")
    print("\t\t\t\tThe same as flag '-t'.")
    print()
    print("\t\tupper()")
    print("\t\t\t\tAll words in upper case.")
    print()
    print("\t\tw2v()")
    print("\t\t\t\tThe same as flag '--w2v'.")
    print()

    

# Print the version option
def printVersion():
    print("rr 1.1")
    print("Licence of University of Minho")
    print("This is a free software: you are free to change and redistribute it.")
    print()
    print("Written by Tiago Barata, Duarte Vilar e Angélica Cunha")
    print("<https://github.com/tiagomqbarata>")
    print("<https://github.com/mishlawi>")
    print("<https://github.com/angelicasc22>")


def perror():
    print("rr: invalid option")
    print("Usage: rr [OPTIONS]... [FILE]...")
    print("Try 'rr --help' for more info.")
    exit(-1)


def perror_file(file):
    print("O ficheiro " + file + " não existe.")
    exit(-1)


def perror_dir(dir):
    print("A diretoria de ficheiros " + dir + " não existe.")
    exit(-1)



def perror_flags(flag):
    if flag == '-t':
        print("Língua não suportada, escolha uma das seguintes opções:")
        print("\tES - Espanhol")
        print("\tEN - Inglês")
        print("\tFR - Francês")
        print("\tIT - Italiano")
        exit(-1)
    elif flag == '-r':
        print("A flag " + flag + " tem de se seguir por um ficheiro de regras")
        print("Try 'rr --help' for more info.")
    elif flag == '--dir':
        print("A flag " + flag + " tem de se seguir por uma diretoria de ficheiros.")
        print("Try 'rr --help' for more info.")
    elif flag == '--spacy' or flag == '--w2v':
        print("As flags --spacy e --w2v são incompatíveis. Só se pode escolher uma para execução.")
        print("Try 'rr --help' for more info.")
    exit(-1)

