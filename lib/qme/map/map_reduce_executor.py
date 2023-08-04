from pymongo import MongoClient
from JSONDocumentBuilder import JSONDocumentBuilder

class Executor:
    def __init__(self, db):
        self.db = MongoClient()[db]

    def measure_def(self, measure_id):
        measures = self.db['measures']
        measure = measures.find_one({'id': measure_id})
        return measure

    def measure_result(self, measure_id, parameter_values):
        measure = JSONDocumentBuilder(self.measure_def(measure_id), parameter_values)

        records = self.db['records']
        results = records.map_reduce(measure.map_function, measure.reduce_function)
        result = results.find_one()
        value = result['value']

        return {
            'population': int(value['i']),
            'denominator': int(value['d']),
            'numerator': int(value['n']),
            'exceptions': int(value['e'])
        }
