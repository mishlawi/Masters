from unidecode import unidecode

def acentos(text):
    return unidecode(text)

def lower(text):
    return text.lower()

import emoji

def text2emoji(text):
    return emoji.emojize(text,language='pt')

from googletrans import Translator

def translate(text, lang):
    translator = Translator()
    text = translator.translate(text, dest=lang.lower())
    return text.text

from re import * 
import sys

text = open(sys.argv[1], 'r', encoding='utf-8').read()
text = sub(r'\bteste\b', '__test__', text)
text = sub(r'\batum\b', '__tuna__', text)
text = sub(r'\bverde\b', '__vermelho__', text)
text = sub(r'\bvermelho\b', '__azul__', text)
text = acentos(text)
text = lower(text)
text = text2emoji(text)
text = sub(r':', '', text)
text = sub(r'__(.+?)__', r'\1', text)
# translate(text, 'en')
print(text)
