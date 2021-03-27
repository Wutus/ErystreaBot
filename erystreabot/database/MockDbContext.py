import pymongo
import os
from typing import Dict

class MockDbContext:

    def __init__(self, patterns: Dict[str, str]):
        self.patterns = patterns

    def getAllReplacers(self, collection: str):
        return self.patterns
