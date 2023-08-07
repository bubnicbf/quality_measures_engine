from py_mini_racer import py_mini_racer

class Builder:
    YEAR_IN_SECONDS = 365 * 24 * 60 * 60

    def __init__(self, measure_def, params):
        self.measure_def = measure_def
        self.id = measure_def['id']
        self.parameters = {}
        self.measure_def.setdefault('parameters', {})

        for parameter, value in self.measure_def['parameters'].items():
            if parameter not in params:
                raise ValueError(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = params[parameter]

        ctx = py_mini_racer.JSContext()
        ctx.execute(f"year = {self.YEAR_IN_SECONDS}")

        for key, param in self.parameters.items():
            ctx.execute(f"{key} = {param}")

        self.measure_def.setdefault('calculated_dates', {})

        for parameter, value in self.measure_def['calculated_dates'].items():
            self.parameters[parameter] = ctx.execute(value)

        self.property_prefix = f'this.measures["{self.id}"].'

    def map_function(self):
        return (
            f"function () {{\n"
            f"  var value = {{i: 0, d: 0, n: 0, e: 0}};\n"
            f"  if {self.population()} {{\n"
            f"    value.i++;\n"
            f"    if {self.denominator()} {{\n"
            f"      value.d++;\n"
            f"      if {self.numerator()} {{\n"
            f"        value.n++;\n"
            f"      }} else if {self.exception()} {{\n"
            f"        value.e++;\n"
            f"        value.d--;\n"
            f"      }}\n"
            f"    }}\n"
            f"  }}\n"
            f"  emit(null, value);\n"
            f"}};\n"
        )

    REDUCE_FUNCTION = (
        "function (key, values) {\n"
        "  var total = {i: 0, d: 0, n: 0, e: 0};\n"
        "  for (var i = 0; i < values.length; i++) {\n"
        "    total.i += values[i].i;\n"
        "    total.d += values[i].d;\n"
        "    total.n += values[i].n;\n"
        "    total.e += values[i].e;\n"
        "  }\n"
        "  return total;\n"
        "};\n"
    )

    def reduce_function(self):
        return self.REDUCE_FUNCTION

    def population(self):
        return self.javascript(self.measure_def['population'])

    def denominator(self):
        return self.javascript(self.measure_def['denominator'])

    def numerator(self):
        return self.javascript(self.measure_def['numerator'])

    def exception(self):
        return self.javascript(self.measure_def.get('exception', {}))

    def javascript(self, expr):
        if 'query' in expr:
            query = expr['query']
            triple = self.leaf_expr(query)
            property_name = self.munge_property_name(triple[0])
            return f'({property_name}{triple[1]}{triple[2]})'
        elif len(expr) == 1:
            operator = list(expr.keys())[0]
            operands = [self.javascript(arg) for arg in expr[operator]]
            js_operator = self.get_operator(operator)
            return '(' + js_operator.join(operands) + ')'
        elif not expr:
            return '(false)'
        else:
            raise ValueError(f"Unexpected number of keys in: {expr}")

    def munge_property_name(self, name):
        if name == 'birthdate':
            return f'this.{name}'
        else:
            return self.property_prefix + name

    def leaf_expr(self, query):
        property_name = list(query.keys())[0]
        value_expression = query[property_name]
        if isinstance(value_expression, dict):
            operator = list(value_expression.keys())[0]
            value = value_expression[operator]
            return (property_name, self.get_operator(operator), self.get_value(value))
        else:
            return (property_name, '==', self.get_value(value_expression))

    def get_operator(self, operator):
        ops = {
            '_eql': '==',
            '_gt': '>',
            '_gte': '>=',
            '_lt': '<',
            '_lte': '<=',
            'and': '&&',
            'or': '||'
        }
        return ops.get(operator, None)

    def get_value(self, value):
        if isinstance(value, str) and value.startswith('@'):
            return str(self.parameters[value[1:]])
        elif value is None:
            return 'null'
        else:
            return str(value)


# Usage:
# measure_def and params should be dictionaries as per the provided Ruby code structure.
# builder = Builder(measure_def, params)
# print(builder.map_function())
