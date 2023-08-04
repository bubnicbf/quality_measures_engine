from QME import Measure

class Builder:
    def __init__(self, measure_def, params):
        self.measure_def = measure_def
        self.measure = Measure(measure_def, params)
        self.property_prefix = 'measures.' + self.measure.id + '.'

    def population(self):
        return self.javascript(self.measure_def['population'])

    def denominator(self):
        return self.javascript(self.measure_def['denominator'])

    def numerator(self):
        return self.javascript(self.measure_def['numerator'])

    def exception(self):
        return self.javascript(self.measure_def['exception'])

    def javascript(self, expr):
        if 'query' in expr:
            # leaf node
            query = expr['query']
            triple = self.leaf_expr(query)
            return self.property_prefix + triple[0] + triple[1] + triple[2]
        else:
            # logical operator $and, $or etc
            return ''

    def leaf_expr(self, query):
        property_name = list(query.keys())[0]
        property_value_expression = query[property_name]
        if isinstance(property_value_expression, dict):
            operator = list(property_value_expression.keys())[0]
            value = property_value_expression[operator]
            return [property_name, self.get_operator(operator), self.get_value(value)]
        else:
            return [property_name, '==', self.get_value(property_value_expression)]

    @staticmethod
    def get_operator(operator):
        operators = {'$gt': '>', '$gte': '>=', '$lt': '<', '$lte': '<='}
        if operator not in operators:
            raise ValueError(f"Unknown operator: {operator}")
        return operators[operator]

    def get_value(self, value):
        if isinstance(value, str) and value[0] == '@':
            return str(self.measure.parameters[value[1:]].value)
        else:
            return str(value)
