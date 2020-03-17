# -*- coding: utf-8 -*-
from datetime import date

def muestra_item_guardado(item):
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('{} ha sido agregado a la lista!'.format(item))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    

def Imprime_datos(Titulo = '',Referer = '', Infringing = '', Cantante = '', Fecha = '', Album = ''):
    if Fecha == '':
        Fecha = date.today().strftime("%d %B, %Y")
        
    print('\n********************************************DATOS********************************************')
    print('infringing: ' + str(Infringing))
    print('referer: ' + str(Referer))
    print('titulo: ' + str(Titulo))
    print('fecha: ' + str(Fecha))
    print('cantante: ' + str(Cantante))
    print('Album: ' + str(Album))
    print('**********************************************************************************************\n')