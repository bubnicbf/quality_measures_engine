class JsonQueryExecutor:
    def __init__(self, db):
        self.db = db

    def measure_def(self, measure_id):
        measures = self.db['measures']
        # Assuming the database client supports the find method like pymongo
        return measures.find({'id': str(measure_id)})[0]

    def measure_result(self, measure_id, parameter_values):
        jdb = JSONDocumentBuilder(self.measure_def(measure_id), parameter_values)
        collection = self.db['records']
        result = {}
        
        # Using pymongo or equivalent, we can directly get the count
        result['numerator'] = collection.find(jdb.numerator_query).count()
        result['denominator'] = collection.find(jdb.denominator_query).count()
        result['population'] = collection.find(jdb.initial_population_query).count()

        exclusions_query = jdb.exclusions_query
        if not exclusions_query:
            result['exceptions'] = 0
        else:
            result['exceptions'] = collection.find(exclusions_query).count()

        return result

