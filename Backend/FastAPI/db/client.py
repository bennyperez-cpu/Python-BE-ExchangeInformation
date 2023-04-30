from pymongo import MongoClient
#Base de Datos Local
# db_client = MongoClient("mongodb://192.168.1.51:27017/").local

#Base de Datos Remota
db_client = MongoClient("mongodb+srv://mrbennyhammer:mrbennyhammer@cluster0.qwlud3w.mongodb.net/?retryWrites=true&w=majority").test

