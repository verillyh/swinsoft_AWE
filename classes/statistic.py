import itertools
from enum import Enum

class Aggregation(Enum):
    a = 1

class Statistic:
    _id_counter = itertools.count(start=-1)
    def __init__(self):
        self.statisticID = next(Statistic._id_counter)
        self.data = []
        self.filters = []
        self.aggregations = []

    def fetchAllData():

        return False
    
    def visualize():

        return False
    
    def aggregate():

        return False
    
    def filtering():

        return False
    