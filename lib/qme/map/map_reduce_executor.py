from Builder import Builder

class Executor:
    def __init__(self, db):
        self.db = db

    def get_measure_def(self, measure_id):
        measures = self.db['measures']
        return measures.find_one({'id': measure_id})

    def execute(self, measure_id, parameter_values):
        measure = Builder(self.get_measure_def(measure_id), parameter_values)

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
