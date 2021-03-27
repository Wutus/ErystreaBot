import pymongo
import os


class MockDbContext:

    def __init__(self, patterns: Dict[str, str]):
        self.patterns = patterns

    def getAllReplacers(self, collection: str):
        return patterns

    def __initDatabase(self, collection: str, entities):
        self.context[collection].insert_many(entities)