from typing import Any, Dict, List, Union
from qme.measure import Measure

class Builder:
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

    def __init__(self, measure_def: Dict[str, Any], params: Dict[str, Any]):
        self.measure_def = measure_def
        self.measure = Measure(measure_def, params)
        self.property_prefix = f'this.measures["{self.measure.id}"].'

    def map_function(self) -> str:
        return (
            "function () {\n" +
            "  var value = {i: 0, d: 0, n: 0, e: 0};\n" +
            f"  if {self.population} {{\n" +
            "    value.i++;\n" +
            f"    if {self.denominator} {{\n" +
            "      value.d++;\n" +
            f"      if {self.numerator} {{\n" +
            "        value.n++;\n" +
            f"      }} else if {self.exception} {{\n" +
            "        value.e++;\n" +
            "        value.d--;\n" +
            "      }\n" +
            "    }\n" +
            "  }\n" +
            "  emit(null, value);\n" +
            "};\n"
        )

    def reduce_function(self) -> str:
        return self.REDUCE_FUNCTION

    def population(self) -> str:
        return self.javascript(self.measure_def['population'])

    def denominator(self) -> str:
        return self.javascript(self.measure_def['denominator'])

    def numerator(self) -> str:
        return self.javascript(self.measure_def['numerator'])

    def exception(self) -> str:
        return self.javascript(self.measure_def['exception'])

    def javascript(self, expr: Dict[str, Any]) -> str:
        if 'query' in expr:
            # leaf node
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
            raise ValueError(f"Unexpected number of keys in: {expr}")

    def munge_property_name(self, name: str) -> str:
        return f'this.{name}' if name == 'birthdate' else f'{self.property_prefix}{name}'

    def logical_expr(self, operator: str, args: List[Dict[str, Any]]) -> List[str]:
        return [self.get_operator(operator)] + [self.javascript(arg) for arg in args]

    def leaf_expr(self, query: Dict[str, Any]) -> List[str]:
        property_name = list(query.keys())[0]
        property_value_expression = query[property_name]
        if isinstance(property_value_expression, dict):
            operator = list(property_value_expression.keys())[0]
            value = property_value_expression[operator]
            return [property_name, self.get_operator(operator), self.get_value(value)]
        else:
            return [property_name, '==', self.get_value(property_value_expression)]

    def get_operator(self, operator: str) -> str:
        operators = {
            '_gt': '>',
            '_gte': '>=',
            '_lt': '<',
            '_lte': '<=',
            'and': '&&',
            'or': '||'
        }
        return operators.get(operator, f"Unknown operator: {operator}")

    def get_value(self, value: Union[str, int]) -> str:
        if isinstance(value, str):
            if value[0] == '@':
                return str(self.measure.parameters[value[1:]])
            else:
                return f'"{value}"'
        else:
            return str(value)
