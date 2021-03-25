import pymongo

class DbContext:
    
    def __init__(self, conString: str, dbName: str):
        self.context = pymongo.MongoClient(conString)[dbName]

    
    def getReplacer(key: str):
        return self.context["regex-replacer"].find({}, {"key": key})

    
    def insertReplacer(key: str, response: str):
        entity = {"key": key, "response": response}
        return self.context["regex-replacer"].insert_one(entity)