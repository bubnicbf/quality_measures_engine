from PyV8 import JSContext

class JSONDocumentBuilder:
    def __init__(self, measure_json, parameters={}):
        self.measure_json = measure_json
        self.parameters = parameters
        self.measure_id = measure_json['id']
        self.calculated_dates = {}

        if parameters:
            self.calculate_dates()

    def calculate_dates(self):
        ctx = JSContext()
        for key, value in self.parameters.items():
            ctx.locals[key] = value

        ctx.locals['year'] = 365 * 24 * 60 * 60  # TODO: Replace this with a js file that has all constants

        for key, value in self.measure_json.get("calculated_dates", {}).items():
            self.calculated_dates[key] = ctx.eval(value)

    def create_query(self, definition_json, args={}):
        if 'and' in definition_json:
            for operand in definition_json['and']:
                self.create_query(operand, args)
        elif 'or' in definition_json:
            operands = []
            for operand in definition_json['or']:
                operands.append(self.create_query(operand))
            args['$or'] = operands
        elif 'query' in definition_json:
            self.process_query(definition_json['query'], args)
        
        return args

    def process_query(self, definition_json, args):
        if len(definition_json) > 1:
            raise Exception('A query should have only one property')

        query_property = list(definition_json.keys())[0]
        document_key = self.transform_query_property(query_property)
        document_value = None
        query_value = definition_json[query_property]
        if isinstance(query_value, dict):
            if len(query_value) > 1:
                raise Exception('A query value should only have one property')

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
        # TODO What do we do with special case fields - the stuff we are keeping at the patient level?
        if property_name in ['birthdate']:
            return property_name
        else:
            return f"measures.{self.measure_id}.{property_name}"

    def substitute_variables(self, value):
        if isinstance(value, str) and value[0] == '@':
            variable_name = value[1:]
            return self.calculated_dates[variable_name]
        else:
            return value
