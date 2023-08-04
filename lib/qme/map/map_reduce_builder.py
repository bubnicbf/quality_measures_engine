from execjs import compile
import json

class Builder:
    YEAR_IN_SECONDS = 365 * 24 * 60 * 60
    REDUCE_FUNCTION = """
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
    """

    def __init__(self, measure_def, params):
        self.measure_def = measure_def
        self.id = measure_def['id']
        self.parameters = {}
        measure_def.setdefault('parameters', {})
        for parameter, value in measure_def['parameters'].items():
            if parameter not in params:
                raise ValueError(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = params[parameter]

        context = compile("""
            var YEAR_IN_SECONDS = {year};
            var parameters = {params};
            parameters;
        """.format(year=self.YEAR_IN_SECONDS, params=json.dumps(self.parameters)))
        
        self.parameters = json.loads(context.eval("parameters"))

        measure_def.setdefault('calculated_dates', {})
        for parameter, value in measure_def['calculated_dates'].items():
            self.parameters[parameter] = context.eval(value)

        self.property_prefix = 'this.measures["' + self.id + '"].'

    def map_function(self):
        return (
            "function () {\n" +
            "  var value = {i: 0, d: 0, n: 0, e: 0};\n" +
            "  if " + self.population() + " {\n" +
            "    value.i++;\n" +
            "    if " + self.denominator() + " {\n" +
            "      value.d++;\n" +
            "      if " + self.numerator() + " {\n" +
            "        value.n++;\n" +
            "      } else if " + self.exception() + " {\n" +
            "        value.e++;\n" +
            "        value.d--;\n" +
            "      }\n" +
            "    }\n" +
            "  }\n" +
            "  emit(null, value);\n" +
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
        return self.javascript(self.measure_def['exception'])

    def javascript(self, expr):
        if 'query' in expr:
            # leaf node
            query = expr['query']
            triple = self.leaf_expr(query)
            property_name = self.munge_property_name(triple[0])
            return '(' + property_name + triple[1] + triple[2] + ')'
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
            raise Exception("Unexpected number of keys in: {}".format(expr))

    def munge_property_name(self, name):
        if name == 'birthdate':
            return 'this.' + name
        else:
            return self.property_prefix + name

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

    def get_operator(self, operator):
        if operator == '_gt':
            return '>'
        elif operator == '_gte':
            return '>='
        elif operator == '_lt':
            return '<'
        elif operator == '_lte':
            return '<='
        elif operator == 'and':
            return '&&'
        elif operator == 'or':
            return '||'
        else:
            raise Exception("Unknown operator: {}".format(operator))

    def get_value(self, value):
        if isinstance(value, str) and value[0] == '@':
            return str(self.parameters[value[1:]])
        elif isinstance(value, str):
            return '"' + value + '"'
        else:
            return str(value)
