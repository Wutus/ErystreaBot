import pymongo
import os

class DbContext:
        
    def __init__(self, conString: str = os.environ["connectionString"], dbName: str = os.environ["databaseName"]):
        self.context = pymongo.MongoClient(conString)[dbName]

    
    def getReplacer(self, collection: str, dbName: str, key: str):
        test = {"key": key}
        return self.context[collection].find_one(test)

    
    def insertReplacer(self, collection: str, key: str, response: str):
        entity = {"key": key, "response": response}
        return self.context[collection].insert_one(entity)


    def __initDatabase(self, collection: str, entities):
        self.context[collection]insert_many(entities)

if(__name__ == "__main__"):
    context = DbContext("mongodb://localhost:27017", "erystrea-bot")
    
    