class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, measure_id, parameter_values):
        measures = self.db['measures']
        measure_def = measures.find_one({'id': measure_id})
        measure = Builder(measure_def, parameter_values)

        records = self.db['records']
        results = records.map_reduce(measure.map_function, measure.reduce_function, "tempResults")
        result = results.find_one()

        print(f" Population: {int(result['value']['i'])}")
        print(f"Denominator: {int(result['value']['d'])}")
        print(f"  Numerator: {int(result['value']['n'])}")
        print(f" Exceptions: {int(result['value']['e'])}")
