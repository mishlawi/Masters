import emoji

def emoji2text(text):
    return emoji.demojize(text,language='pt')
