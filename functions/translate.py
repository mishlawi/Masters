from googletrans import Translator

def translate(text, lang):
    translator = Translator()
    text = translator.translate(text, dest=lang.lower())
    return text.text
