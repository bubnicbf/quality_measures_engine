import os
import glob
import json
import unittest
from time import gmtime, mktime
from pymongo import MongoClient
from Executor import Executor

class TestExecutor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = MongoClient('localhost', 27017).test
        cls.measures = glob.glob('measures/*')

    def test_should_produce_the_expected_results_for_each_measure(self):
        print("\n")
        for dir in self.measures:
            # load db with measure and sample patient records
            measure_file = glob.glob(os.path.join(dir, '*.json'))[0]
            patient_files = glob.glob(os.path.join(dir, 'patients', '*.json'))
            with open(measure_file, 'r') as f:
                measure = json.load(f)
            measure_id = measure['id']
            print(f"Validating measure {measure_id}")
            self.db.drop_collection('measures')
            self.db.drop_collection('records')
            measure_collection = self.db.create_collection('measures')
            record_collection = self.db.create_collection('records')
            measure_collection.insert_one(measure)
            for patient_file in patient_files:
                with open(patient_file, 'r') as f:
                    patient = json.load(f)
                record_collection.insert_one(patient)

            # load expected results
            result_file = os.path.join(dir, 'result', 'result.json')
            with open(result_file, 'r') as f:
                expected = json.load(f)

            # evaluate measure using Map/Reduce and validate results
            executor = Executor(self.db)
            result = executor.measure_result(measure_id, {'effective_date': int(mktime(gmtime(2010, 9, 19)))})
            self.assertEqual(result['population'], expected['initialPopulation'])
            self.assertEqual(result['numerator'], expected['numerator'])
            self.assertEqual(result['denominator'], expected['denominator'])
            self.assertEqual(result['exceptions'], expected['exclusions'])
            print(" - done\n")


if __name__ == '__main__':
    unittest.main()
