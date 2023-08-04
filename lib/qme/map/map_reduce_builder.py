from QME import Measure

class Builder:
    def __init__(self, measure_def, params):
        self.measure_def = measure_def
        self.measure = Measure(measure_def, params)
        self.property_prefix = f'measures["{self.measure.id}"].'

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
            return f'({self.property_prefix}{triple[0]}{triple[1]}{triple[2]})'
        elif len(expr) == 1:
            operator = list(expr.keys())[0]
            result = self.logical_expr(operator, expr[operator])
            operator = result.pop(0)
            js = '('
            for index, operand in enumerate(result):
                if index > 0:
                    js += operator
                js += operand
            js += ')'
            return js
        elif len(expr) == 0:
            return '(false)'
        else:
            raise ValueError(f"Unexpected number of keys in: {expr}")

    def logical_expr(self, operator, args):
        operands = [self.javascript(arg) for arg in args]
        return [self.get_operator(operator)] + operands

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
        operators = {
            '$gt': '>',
            '$gte': '>=',
            '$lt': '<',
            '$lte': '<=',
            '$and': '&&',
            '$or': '||'
        }
        if operator in operators:
            return operators[operator]
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def get_value(self, value):
        if isinstance(value, str):
            if value[0] == '@':
                return str(self.measure.parameters[value[1:]].value)
            else:
                return f'"{value}"'
        else:
            return str(value)
