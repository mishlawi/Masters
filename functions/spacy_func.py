import spacy
from re import *

def spacy_func(texto):
    npl = spacy.load("pt_core_news_lg")

    texto = sub(r"\n{2,}", "=", texto)
    texto = sub(r'\n', ' ', texto)
    texto = sub(r'=', '\n', texto)

    res = ""

    for linha in split(r'\n', texto):
        for phrase in npl(linha).sents:
            n = 1
            state = 0
            for token in phrase:
                if state == 0:
                    if token.ent_iob_ == 'B':
                        name = token.text
                        state = 1
                        pos = token.pos_
                        ent_type = token.ent_type_
                    elif token.ent_iob_ == "O":
                        res += f"{n}\t{token.text}\t{token.lemma_}\t{token.pos_}\n"
                elif state == 1:
                    if token.ent_iob_ == "I":
                        name += "_" + token.text
                    elif token.ent_iob_ == "O":
                        res += f"{n}\t{name}\t{pos}\t{ent_type}\n"
                        n+=1
                        res += f"{n}\t{token.text}\t{token.lemma_}\t{token.pos_}\n"
                        state = 0
                    elif token.ent_iob_ == "B":
                        res += f"{n}\t{name}\t{pos}\t{ent_type}\n"
                        name = token.text
                        pos = token.pos_
                        ent_type = token.ent_type_
                        state = 1
                n += 1
            if state == 1:
                res += f"{n}\t{name}\t{pos}\t{ent_type}\n"
                state = 0
            res += "\n"
    
    return res
