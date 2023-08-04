from execjs import compile

# Represents a quality measure definition
class Measure:

    SUPPORTED_PROPERTY_TYPES = {'long': 'long', 'boolean': 'boolean'}

    @classmethod
    def get_type(cls, name):
        if name in cls.SUPPORTED_PROPERTY_TYPES:
            return cls.SUPPORTED_PROPERTY_TYPES[name]
        else:
            raise ValueError(f"Unsupported property type: {name}")

    YEAR_IN_SECONDS = 365 * 24 * 60 * 60

    def __init__(self, measure, params):
        self.id = measure['id']
        self.name = measure['name']
        self.steward = measure['steward']
        self.properties = {}
        measure.setdefault('properties', {})
        for property, value in measure['properties'].items():
            self.properties[property] = Property(value['name'],
                                                 value['type'],
                                                 value['codes'])
        self.parameters = {}
        measure.setdefault('parameters', {})
        for parameter, value in measure['parameters'].items():
            if parameter not in params:
                raise ValueError(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = Parameter(value['name'],
                                                   value['type'],
                                                   params[parameter])

        ctx = compile("""
            function calculate(value, year) {
                return eval(value)
            }
        """)

        measure.setdefault('calculated_dates', {})
        for parameter, value in measure['calculated_dates'].items():
            self.parameters[parameter] = Parameter(parameter, 'long', ctx.call('calculate', value, self.YEAR_IN_SECONDS))

# Represents a property of a quality measure
class Property:

    def __init__(self, name, type, codes):
        self.name = name
        self.type = Measure.get_type(type)
        self.codes = codes

# Represents a parameter of a quality measure
class Parameter:

    def __init__(self, name, type, value):
        self.name = name
        self.type = Measure.get_type(type)
        self.value = value
