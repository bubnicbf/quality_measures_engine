import unittest
import pymongo
import os
import json
import time

# Assuming there's a pythonic version of QME::MapReduce::Executor
from qme_mapreduce_executor import QMEMapReduceExecutor 

class TestQMEMapReduceExecutor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_host = os.environ.get('TEST_DB_HOST', 'localhost')
        cls.client = pymongo.MongoClient(db_host, 27017)
        cls.db = cls.client['test']
        cls.measures = [f.path for f in os.scandir('measures') if f.is_dir()]

    def test_expected_results_for_each_measure(self):
        print("\n")
        for dir in self.measures:
            # Load db with measure and sample patient records
            files = [f.path for f in os.scandir(dir) if f.is_file() and f.name.endswith('.json')]
            self.assertEqual(len(files), 1)
            measure_file = files[0]
            patient_files = [f.path for f in os.scandir(os.path.join(dir, 'patients')) if f.is_file() and f.name.endswith('.json')]
            
            with open(measure_file, 'r') as mf:
                measure = json.load(mf)
            measure_id = measure['id']
            print(f"Validating measure {measure_id}")
            
            self.db.drop_collection('measures')
            self.db.drop_collection('records')
            
            measure_collection = self.db['measures']
            record_collection = self.db['records']
            
            measure_collection.insert_one(measure)
            for patient_file in patient_files:
                with open(patient_file, 'r') as pf:
                    patient = json.load(pf)
                record_collection.insert_one(patient)

            # Load expected results
            result_file = os.path.join(dir, 'result', 'result.json')
            with open(result_file, 'r') as rf:
                expected = json.load(rf)
            
            executor = QMEMapReduceExecutor(self.db)
            result = executor.measure_result(measure_id, effective_date=int(time.mktime(time.strptime("2010-09-19", "%Y-%m-%d"))))
            
            # Compare results
            self.assertEqual(result['population'], expected['initialPopulation'])
            self.assertEqual(result['numerator'], expected['numerator'])
            self.assertEqual(result['denominator'], expected['denominator'])
            self.assertEqual(result['exceptions'], expected['exclusions'])
            
            print(" - done")

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

if __name__ == '__main__':
    unittest.main()
