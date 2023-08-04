import time
from pymongo import MongoClient
from map_reduce_executor import MapReduceExecutor

def test_executor():
    db = MongoClient('localhost', 27017)['test']
    executor = MapReduceExecutor(db)

    result = executor.execute('0043', {"effective_date": time.mktime(time.strptime('2010-09-19', '%Y-%m-%d'))})

    assert result['population'] == 3
    assert result['numerator'] == 1
    assert result['denominator'] == 2
    assert result['exceptions'] == 0
