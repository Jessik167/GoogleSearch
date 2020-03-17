# -*- coding: utf-8 -*-
import pprint
import pymysql
import pymongo
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import loads, dumps
from pymongo.errors import ConnectionFailure

# DATOS PARA MYSQL
DB_HOST_mysql = '3.231.20.132'
DB_USER = 'apdif'
DB_PASSWORD = 'K3XyRwLjPtkui6qJ'
DB_NAME = 'apdif'

# DATOS PARA MONGO
DB_HOST = 'localhost' #'mongodb+srv://APDIF:'+ DB_PASSWORD +'@apdif-hsrgh.mongodb.net/test?retryWrites=true&w=majority'
PORT = 27017

    
def inserta_documento(user_doc):
    c = MongoClient(host=DB_HOST, port=PORT)
    with c:
        db = c.GoogleSearch
        existing_document = db.Gsearch.find_one(user_doc)
        if not existing_document:
            db.Gsearch.insert(user_doc)
            
            
def inserta_termino(art, tb):
    c = MongoClient(host=DB_HOST, port=PORT)
    with c:
        db = c.GoogleSearch
        existing_term = db.Gsearch.find_one({ "$and": [{'_id': art}, {tb: {"$exists":True}}]})
        if not existing_term:
            db.Gsearch.update({"_id": art},
                        {"$set":{tb: {}}})
    
    
def inserta_documentoHOST(user_doc):
    c = MongoClient('mongodb+srv://APDIF:'+ DB_PASSWORD +'@apdif-hsrgh.mongodb.net/test?retryWrites=true&w=majority')
    with c:
        db = c.GoogleSearch
        existing_document = db.Gsearch.find_one(user_doc)
        if not existing_document:
            db.Gsearch.insert(user_doc)
    
    
def inserta_dominio(user_doc, art, tb, dom):
    print()
    c = MongoClient(host=DB_HOST, port=PORT)
    with c:
        db = c.GoogleSearch
        #existing_term = db.Gsearch.find_one({ "$and": [{'_id': art}, {tb + '.' +dom: {"$exists":True}}]})
        #if not existing_term:
        db.Gsearch.update({"_id": art},
                          {"$set":{tb + '.' +dom : user_doc}})  
    return True
    
       
def Busca_documento(art, tb):
    c = MongoClient(host=DB_HOST, port=PORT)
    with c:
        db = c.GoogleSearch
        doc = db.Gsearch.distinct(tb, {'_id': art})
        #pprint.pprint(doc)
        return doc
        
        
def Busca_dominios(art):
    c = MongoClient(host=DB_HOST, port=PORT)
    dominios = []
    with c:
        db = c.GoogleSearch
        doc = db.Gsearch.find_one({'_id': art})
        if doc:
            doc = db.Gsearch.find({'_id': art})
            dum = dumps(doc)
            json = loads(dum)[0]
            #pprint.pprint(json)
            for key in json.keys():
                if key == '_id':
                    continue
                for k in json[key].keys():
                #print(key)
                    try:
                        #print(json[key][k]['Nombre dominio'])
                        nd = json[key][k]['Dominio']
                        if nd not in dominios:
                            dominios.append(nd)
                    except:
                        continue
            return dominios
        else:
            return 'El usuario "{}" no existe.'.format(art)
    
#print(Busca_dominios('Maluma'))


def Busca_dominio(name):
    c = MongoClient(host=DB_HOST, port=PORT)
    db = c.GoogleSearch
    user_doc = db.Gsearch.find_one({'Dominio': name})
    if not user_doc:
        print('No encontró el dominio: {}'.format(name))


def artistas_itunes():
    con = pymysql.connect(DB_HOST_mysql, DB_USER, DB_PASSWORD, DB_NAME)
    
    with con:
        cur = con.cursor()
        sql = ('''SELECT DISTINCT artist FROM `itunes_artist`''')
        cur.execute(sql)

        results = cur.fetchall()

        return results

