class JSONDocumentBuilder:
    def __init__(self, measure_json, parameters=None):
        if parameters is None:
            parameters = {}

        self.measure_json = measure_json
        self.parameters = parameters
        self.measure_id = measure_json['id']
        self.calculated_dates = {}

        if self.parameters:
            self.calculate_dates()

    def calculate_dates(self):
        self.calculated_dates = self.parameters

        # TODO: Replace the following with an appropriate Python method
        # to evaluate JavaScript or a Python-based logic
        # year = 365 * 24 * 60 * 60  # This is a direct translation and might not be needed

        for key, value in self.measure_json["calculated_dates"].items():
            self.calculated_dates[key] = value

    def numerator_query(self):
        result = self.create_query(self.measure_json['numerator'])
        result.update(self.denominator_query())
        return result

    def denominator_query(self):
        result = self.create_query(self.measure_json['denominator'])
        result.update(self.initial_population_query())
        return result

    def initial_population_query(self):
        return self.create_query(self.measure_json['population'])

    def exclusions_query(self):
        return self.create_query(self.measure_json['exception'])

    def create_query(self, definition_json):
        args = {}

        if 'and' in definition_json:
            for operand in definition_json['and']:
                self.create_query(operand, args)

        elif 'or' in definition_json:
            operands = [self.create_query(operand) for operand in definition_json['or']]
            if '$or' in args:
                args['$ne'] = {'$or': operands}
            else:
                args['$or'] = operands

        elif 'query' in definition_json:
            self.process_query(definition_json['query'], args)

        return args

    def process_query(self, definition_json, args):
        if len(definition_json) > 1:
            raise ValueError('A query should have only one property')

        query_property = list(definition_json.keys())[0]
        document_key = self.transform_query_property(query_property)
        query_value = definition_json[query_property]

        if isinstance(query_value, dict):
            if len(query_value) > 1:
                raise ValueError('A query value should only have one property')
            document_value = {list(query_value.keys())[0].replace('_', '$'):
                              self.substitute_variables(list(query_value.values())[0])}
            if document_key in args:
                args[document_key].update(document_value)
            else:
                args[document_key] = document_value
        else:
            document_value = self.substitute_variables(query_value)
            args[document_key] = document_value

    def transform_query_property(self, property_name):
        # TODO: Handle special case fields, this logic might differ based on your application
        if property_name in ['birthdate']:
            return property_name
        else:
            return f"measures.{self.measure_id}.{property_name}"

    def substitute_variables(self, value):
        if isinstance(value, str) and value.startswith('@'):
            variable_name = value[1:]
            return self.calculated_dates[variable_name]
        else:
            return value
