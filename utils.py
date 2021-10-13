import os
import json
import requests


def decode(txt_encode):
    txt = ''
    for u in txt_encode.split('-'):
        txt = txt + chr(int(u))
    return txt


def encode(txt):
    txt_encode = ''
    for u in txt:
        txt_encode = txt_encode + str(ord(u)) + '-'
    return txt_encode[:-1]


def translate(key, lang='fr'):
    '''
        Traduire un mot clé dans données.
    '''
    if not lang:
        # mettre une langue par defaut
        lang = 'fr'

    if not os.path.isfile("langs.json"):
        print("Attention, fichier langs.json n'existe pas")
        return key

    with open("langs.json") as fichier:
        trans = json.load(fichier)

    mot_cle = trans.get(key)

    if mot_cle:
        if mot_cle.get(lang):
            return mot_cle.get(lang)
    return key


def download_file(url, chemin):
    '''
        Telechargement d'un fichier à partir d'une url.
    '''
    # Lancement du requete
    res = requests.get(url, allow_redirects=True)

    # enregistrement du fichier
    with open(chemin, 'wb') as file:
        file.write(res.content)

    return chemin
