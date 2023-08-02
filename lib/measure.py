import json
from py_mini_racer import py_mini_racer

class UnsupportedPropertyTypeError(Exception):
    pass

SUPPORTED_PROPERTY_TYPES = {'long': 'long', 'boolean': 'boolean'}

def get_type(name):
    if name in SUPPORTED_PROPERTY_TYPES:
        return SUPPORTED_PROPERTY_TYPES[name]
    else:
        raise UnsupportedPropertyTypeError(f"Unsupported property type: {name}")


class Measure:
    YEAR_IN_SECONDS = 365*24*60*60

    def __init__(self, measure, params):
        self.id = measure['id']
        self.name = measure['name']
        self.steward = measure['steward']
        self.properties = {}
        for property, value in measure['properties'].items():
            self.properties[property] = Property(value['name'], value['type'], value['codes'])
        
        self.parameters = {}
        for parameter, value in measure['parameters'].items():
            if parameter not in params:
                raise Exception(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = Parameter(value['name'], value['type'], params[parameter])

        ctx = py_mini_racer.MiniRacer()
        ctx.eval(f"var year={self.YEAR_IN_SECONDS};")
        for key, param in self.parameters.items():
            ctx.eval(f"var {key}={param.value};")

        for parameter, value in measure.get('calculated_dates', {}).items():
            self.parameters[parameter] = Parameter(parameter, 'long', ctx.eval(value))


class Property:
    def __init__(self, name, type, codes):
        self.name = name
        self.type = get_type(type)
        self.codes = codes


class Parameter:
    def __init__(self, name, type, value):
        self.name = name
        self.type = get_type(type)
        self.value = value
