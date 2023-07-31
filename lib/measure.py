SUPPORTED_PROPERTY_TYPES = {'long': 'long', 'boolean': 'boolean'}

class Measure:
    def __init__(self, measure, params):
        self.id = measure['id']
        self.name = measure['name']
        self.steward = measure['steward']
        self.properties = {}
        for property, value in measure["properties"].items():
            self.properties[property] = Property(value['name'], value['type'], value['codes'])
        self.parameters = {}
        for parameter, value in measure["parameters"].items():
            if parameter not in params:
                raise Exception(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = Parameter(value['name'], value['type'], params[parameter])

class Property:
    def __init__(self, name, type, codes):
        self.name = name
        if type in SUPPORTED_PROPERTY_TYPES:
            self.type = SUPPORTED_PROPERTY_TYPES[type]
        else:
            raise Exception(f"Unsupported property type: {type}")
        self.codes = codes

class Parameter:
    def __init__(self, name, type, value):
        self.name = name
        if type in SUPPORTED_PROPERTY_TYPES:
            self.type = SUPPORTED_PROPERTY_TYPES[type]
        else:
            raise Exception(f"Unsupported parameter type: {type}")
        self.value = value
