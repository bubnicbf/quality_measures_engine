import json
from PyV8 import JSContext

# Represents a quality measure definition
class Measure:
    YEAR_IN_SECONDS = 365 * 24 * 60 * 60

    def __init__(self, measure, params):
        # Parses the supplied measure definition, extracts the measure properties
        # and calculates the values of any calculated dates. <tt>measure</tt> is
        # expected to be a dictionary equivalent to that obtained from applying json.loads
        # to a JSON measure definition. The <tt>params</tt> dictionary should contain a
        # value for each parameter listed in the measure.
        self.id = measure.get('id')
        self.name = measure.get('name')
        self.steward = measure.get('steward')
        self.parameters = {}
        measure_parameters = measure.get('parameters', {})
        for parameter, value in measure_parameters.items():
            if parameter not in params:
                raise Exception(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = Parameter(value.get('name'), params[parameter])

        ctx = JSContext()
        ctx.enter()
        ctx.locals.year = self.YEAR_IN_SECONDS
        for key, param in self.parameters.items():
            ctx.locals[key] = param.value

        measure_calculated_dates = measure.get('calculated_dates', {})
        for parameter, value in measure_calculated_dates.items():
            self.parameters[parameter] = Parameter(parameter, ctx.eval(value))

# Represents a parameter of a quality measure
class Parameter:
    def __init__(self, name, value):
        self.name = name
        self.value = value
