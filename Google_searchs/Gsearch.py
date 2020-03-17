# -*- coding: utf-8 -*-
'''
Created on 21 ene. 2020

@author: APDIF
'''
import re
import time
import json
import copy
import Controlador as c
from selenium import webdriver
from Vista import Imprime_datos, muestra_item_guardado
from urllib.parse import urlparse
from Verificador import separa_titulo, strip_accents


# CIERRA TODAS LAS TABS DEL DRIVER, EXCEPTO LA PRIMERA (GOOGLE)
def close_taps(driver):
    original_handle = driver.window_handles[0]
    for handle in driver.window_handles:
        if handle != original_handle:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(original_handle)
    

# BUSCA LOS IFRAMES DE LA PÁGINA
def busca_iframes(driver):
    infringing = []
    if driver.find_elements_by_tag_name("iframe"):
        for i in driver.find_elements_by_tag_name("iframe"):
            try:
                attr = i.get_attribute('src')
                if attr.find('youtube') == -1 and attr.find('facebook') == -1 and attr.find('twitter') == -1 and attr.find('google') == -1 and attr.find('apk') == -1 and attr.find('promotion') == -1:
                    if attr != '' and attr.endswith('.php') == False and attr.endswith('.html') == False and attr.find('void') == -1:
                        infringing.append(attr)
            except:
                continue
        return infringing
    else:
        return infringing

# ENCUENTRA EL TEXTO PADRE DEL BOTON, CUYO TEXTO CONTENGA EL NOMBRE DEL ARTISTA
def Encuentra_texto(driver, artista):
    i = 0
    padre = driver.find_element_by_xpath('..')
    while i < 5:
        textos = padre.find_elements_by_xpath(".//*[contains(text(), '" + artista + "')]")
        if len(textos) == 0:
            textos = padre.find_elements_by_xpath(".//*[contains(text(), '" + artista.lower() + "')]")
            if len(textos) == 0:
                textos = padre.find_elements_by_xpath(".//*[contains(text(), '" + artista.upper() + "')]")
        if textos:
            for t in textos:
                texto = re.search('.*[.*]*{}.*'.format(artista), t.text)
                if texto is None:
                    texto = re.search('.*[.*]*{}.*'.format(artista.lower()), t.text)
                    if texto is None:
                        texto = re.search('.*[.*]*{}.*'.format(artista.upper()), t.text)
                if texto:
                    #print(texto.group(0))
                    return texto.group(0)
        i += 1
        padre = padre.find_element_by_xpath('..')
    return False
    
    
# ENCUENTRA LOS BOTONES CON EL TEXTO "DESCARGAR"
def find_downloads(driver, artista):
    for d in driver.find_elements_by_xpath(".//*[contains(text(), 'Opciones')]") or driver.find_elements_by_xpath(".//*[contains(text(), 'Descargar')]") or driver.find_elements_by_xpath(".//*[contains(text(), 'Download')]"):
        #print(d.text)
        try:
            if d.text.find('Descargar música') != -1 or d.text.find('Descargar musica') != -1 or d.text.find('MP3 GRATIS') != -1 or d.text == '':
                continue
            d.click()
            time.sleep(1)
            referer = driver.current_url
            try:
                driver.switch_to.window(driver.window_handles[2])
                referer = driver.current_url.strip()
                texto = driver.title.lower().replace('Download ', '').replace('download ', '').replace('MP3', '').replace('mp3', '').replace("'", '')
                infringing = []
                if texto.find(artista.lower()) != -1:
                    time.sleep(3)
                    infringing = busca_iframes(driver) 
                    if len(infringing) == 0:
                        infringing.append(driver.current_url)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                else:
                    if driver.current_url.find('mega') != -1:
                        infringing.append(driver.current_url)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[1])
                    else:
                        if texto.find('donde descargar') != -1 or texto.find('para descargar') != -1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[1])
                            texto = Encuentra_texto(d, artista)
                            time.sleep(4)
                            infringing = busca_iframes(driver)
                        else:
                            referer = driver.current_url
                            time.sleep(7)
                            try:
                                texto = Encuentra_texto(d, artista)
                            except:
                                pass
                            infringing = busca_iframes(driver)
                            if len(infringing) == 0:
                                infringing.append(driver.current_url)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[1])    
            except:
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(8)
                texto = Encuentra_texto(d, artista)
                infringing = busca_iframes(driver)
            if texto == False:
                texto = ''
            else:
                texto = strip_accents(texto).strip()
                Album = separa_titulo(texto, artista)
            if Album is None:
                Album = ''
            if len(infringing) != 0 and texto != '':
                Imprime_datos(texto, referer, infringing, artista, Album=Album)
                Toma_datos(texto, referer, infringing, Album)
        except:
            continue
    close_taps(driver)
    driver.switch_to.window(driver.window_handles[0])
    return driver



# TOMA LOS DATOS DEL DOMINIO
def Toma_datos(texto, referer, infringing, Album):
    Contenido['Titulo'] = texto
    Contenido['Album'] = Album
    Contenido['Referer'] = referer
    Contenido['Infringing'] = infringing
    Dominio['Contenido'].append(copy.deepcopy(Contenido))

    
    
# BUSCA POR URL Y ARTISTA ESPECÍFICO
def busca_url_artista(url, artista, term):
    global Contenido
    global Dominio
    Contenido ={}
    Dominio = {'Contenido':[]}
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
    driver.get('https://www.google.com/search?q={}+{}'.format(artista, term))
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[1])
    find_downloads(driver,artista)
    driver.quit()


# BUSCA EN LAS PRIMERAS TRES PÁGINAS DE GOOGLE CADA ARTISTA
def busca_todos(artistas, url, PClave):
    global Contenido
    global Dominio
    Contenido ={}
    Documentos = {}
    Dominio = {'Contenido':[]}
    for a in artistas:
        Document_art = {'_id': a[0]}
        c.inserta_documento(Document_art)
        for p in PClave:
            i = 0
            c.inserta_termino(a[0],p)
            TB = a[0] +'+'+ p
            Url_b = url + TB
            #print(Url_b)
            driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
            driver.get(Url_b)
            while i < 3:
                for r in driver.find_elements_by_css_selector("#rso > div div > div.r > a"):
                    #print(r.get_attribute('href'))
                    try:
                        referer = r.get_attribute('href').strip()
                        dom = str(urlparse(referer).scheme + '://' + urlparse(referer).netloc + '/')
                        driver.execute_script("window.open(arguments[0]);", referer)
                        driver.switch_to.window(driver.window_handles[1])
                        driver = find_downloads(driver,a[0])
                        if Dominio['Contenido']:
                            D = urlparse(referer).netloc.replace('www.', '').replace('vww.', '').replace('wvw.', '').replace('.com', '').replace('.pub', '').replace('.org', '').replace('.cc', '').replace('.', '-')
                            Dominio['Dominio'] = dom
                            if c.inserta_dominio(Dominio, a[0], p, D) == True:
                                muestra_item_guardado(D)                         
                        Dominio = {'Contenido':[]}
                        time.sleep(5)
                    except:
                        continue
                    #break
                try:
                    i += 1
                    next_page = driver.find_element_by_id('pnnext')
                    next_page.click()
                except:
                    break
                #break
            driver.quit()
            #break
        #break
    print('Termina')
    



_num_pagina = 1
id_domin = 0
start_urls = ['https://www.google.com/search?q=']
# PALABRAS CLAVE DE BÚSQUEDA PARA CADA ARTISTA
PClave = ['descargar','mp3','download','música gratis','mp3 free', 'descarga directa'] # 
artistas = c.artistas_itunes()
#artistas = [('Maluma',)]


#busca_url_artista('https://musicaq.uno/descargar-musica/2eee6-adele.html', artistas[0][0], PClave[0])
busca_todos(artistas, start_urls[0], PClave)