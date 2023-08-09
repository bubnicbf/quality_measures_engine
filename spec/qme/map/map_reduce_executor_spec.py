import unittest
from pymongo import MongoClient
from Executor import Executor
from time import gmtime, mktime

class TestExecutor(unittest.TestCase):

    def test_should_be_able_to_get_a_query_from_the_database(self):
        db = MongoClient('localhost', 27017)['test']
        e = Executor(db)
        
        r = e.measure_result('0043', {'effective_date': int(mktime(gmtime(2010, 9, 19)))})
        
        self.assertEqual(r['population'], 3)
        self.assertEqual(r['numerator'], 1)
        self.assertEqual(r['denominator'], 2)
        self.assertEqual(r['exceptions'], 0)


if __name__ == '__main__':
    unittest.main()
