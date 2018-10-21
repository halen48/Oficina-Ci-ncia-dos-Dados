#http://api.mongodb.com/python/current/tutorial.html
#https://docs.mongodb.com/manual/reference/method/js-collection/
#https://docs.mongodb.com/manual/reference/operator/query-comparison/

import pymongo
import json

arq_json = open('dataset.json', 'r') 

dados = json.loads(arq_json.read())

client = pymongo.MongoClient('localhost', 27017)
db = client['Exatec2018']

db.Pessoas.insert_many(dados)