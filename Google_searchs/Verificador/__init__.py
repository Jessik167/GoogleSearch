# -*- coding: utf-8 -*-
import unicodedata

def separa_titulo(titulo,art):
    #####SEPARA CANTANTE Y ALBUM#####
    if titulo is not None:
        try:
            s = titulo.split('-')
        except:
            s = titulo.split('–')
        if len(s) > 2:
            album = '-'
        else:
            try:
                album = '-'
                if album.lower().find(art.lower()) != -1 :
                    album = s[0]
                else:
                    album = s[1]
            except:
                album = '-'
        return album
    else:
        return '',''
    
    
def strip_accents(text):
    try:
        text = str(text, 'utf-8')
    except (TypeError, NameError): 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text) 