import pymongo
import os


class DbContext:

    def __init__(self, conString: str, dbName: str):
        self.context = pymongo.MongoClient(conString)[dbName]

    def getReplacer(self, collection: str, dbName: str, key: str):
        test = {"key": key}
        return self.context[collection].find_one(test)

    def insertReplacer(self, collection: str, key: str, response: str):
        entity = {"key": key, "response": response}
        return self.context[collection].insert_one(entity)

    def getAllReplacers(self, collection: str):
        return self.context[collection].find()

    def __initDatabase(self, collection: str, entities):
        self.context[collection].insert_many(entities)
