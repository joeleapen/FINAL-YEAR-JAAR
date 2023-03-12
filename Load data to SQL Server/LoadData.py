'''This LoadData.py script is used to load Json files into MongoDB Database'''
#----------------------INPUT SECTION-----------------------------------------------------

MongoDB_Databasename="MyBankCardsManagerDB"
Original_database_table_name="Original"
Honeypot_database_table_name="SuperOriginal"



#---------------------------------------------------------------------------

#- - - - - -
def install(package):
    # This function will install a package if it is not present
    from importlib import import_module
    try:
        import_module(package)
    except:
        from sys import executable as se
        from subprocess import check_call
        check_call([se,'-m','pip','-q','install',package])


for package in ['pymongo','json']:
    install(package)
#- - - - - -

import pymongo
import json

def loadJSONIntoMongoDB(databasename,jsonPath,collectionName):
    MongoDBClient=pymongo.MongoClient("mongodb://localhost:27017/")
    mydatabase=MongoDBClient[databasename]
    records=[]
    with open(jsonPath) as json_file:
        records=json.load(json_file)
    MongoCollection=mydatabase[collectionName]
    try:
        insertObject=mydatabase.MongoCollection.insert_many(records)
        mydatabase.MongoCollection.rename(collectionName, dropTarget = False)
        #print(insertObject)
    except:
        print("An exception occured while importing Json into MongoDB\nDetails:")
    print("Imported ",collectionName)



loadJSONIntoMongoDB(MongoDB_Databasename,jsonPath='original.json',collectionName=Original_database_table_name)
loadJSONIntoMongoDB(MongoDB_Databasename,jsonPath='superoriginal.json',collectionName=Honeypot_database_table_name)
