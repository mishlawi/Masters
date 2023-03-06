import spacy
from re import *
from nltk.corpus import stopwords


# pre-processamento para word embending
def w2v(texto):
    npl = spacy.load("pt_core_news_lg")
    stop_words = set(stopwords.words('portuguese'))

    texto = sub(r"\n{2,}", "=", texto)
    texto = sub(r'\n', ' ', texto)
    texto = sub(r'=', '\n', texto)

    res = []

    for linha in split(r'\n', texto):
        for phrase in npl(linha).sents:
            lista = []
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
                        lista.append(token.text)
                elif state == 1:
                    if token.ent_iob_ == "I":
                        name += "_" + token.text
                    elif token.ent_iob_ == "O":
                        lista.append(name)
                        n+=1
                        lista.append(token.text)
                        state = 0
                    elif token.ent_iob_ == "B":
                        lista.append(name)
                        name = token.text
                        pos = token.pos_
                        ent_type = token.ent_type_
                        state = 1
                n += 1
            if state == 1:
                lista.append(name)
                state = 0
            lista = [w for w in lista if not w.lower() in stop_words]
            res.append(lista)

    return str(res)
