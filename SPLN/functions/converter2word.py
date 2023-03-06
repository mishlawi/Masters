from num2words import num2words
from re import *

def converter2word(text):
    def nd(x):
        return num2words(x[1],lang='pt')

    text = sub(r'\b(\d+)\b', nd, text )
    return text
