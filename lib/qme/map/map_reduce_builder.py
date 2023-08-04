from Measure import Measure

class Builder:
    def __init__(self, measure_def, params):
        self.measure_def = measure_def
        self.measure = Measure(measure_def, params)
        self.property_prefix = f'this.measures["{self.measure.id}"].'

    def map_function(self):
        return f'''
        function () {{
          var value = {{i: 0, d: 0, n: 0, e: 0}};
          if {self.population} {{
            value.i++;
            if {self.denominator} {{
              value.d++;
              if {self.numerator} {{
                value.n++;
              }} else if {self.exception} {{
                value.e++;
                value.d--;
              }}
            }}
          }}
          emit(null, value);
        }};
        '''

    REDUCE_FUNCTION = '''
    function (key, values) {
      var total = {i: 0, d: 0, n: 0, e: 0};
      for (var i = 0; i < values.length; i++) {
        total.i += values[i].i;
        total.d += values[i].d;
        total.n += values[i].n;
        total.e += values[i].e;
      }
      return total;
    };
    '''

    def reduce_function(self):
        return self.REDUCE_FUNCTION

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
            query = expr['query']
            triple = self.leaf_expr(query)
            property_name = self.munge_property_name(triple[0])
            return f'({property_name}{triple[1]}{triple[2]})'
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
            raise Exception(f"Unexpected number of keys in: {expr}")

    def munge_property_name(self, name):
        return f'this.{name}' if name == 'birthdate' else f'{self.property_prefix}{name}'

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
        switcher = {
            '_gt': '>',
            '_gte': '>=',
            '_lt': '<',
            '_lte': '<=',
            'and': '&&',
            'or': '||',
        }
        return switcher.get(operator, Exception(f"Unknown operator: {operator}"))

    def get_value(self, value):
        if isinstance(value, str) and value[0] == '@':
            return str(self.measure.parameters[value[1:]].value)
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return str(value)
