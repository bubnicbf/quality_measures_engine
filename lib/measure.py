class SUPPORTED_PROPERTY_TYPES:
    types = {'long': 'long', 'boolean': 'boolean'}

    @staticmethod
    def get_type(name):
        if name in SUPPORTED_PROPERTY_TYPES.types:
            return SUPPORTED_PROPERTY_TYPES.types[name]
        else:
            raise Exception(f"Unsupported property type: {name}")

class Measure:
    def __init__(self, measure, params):
        self.id = measure['id']
        self.name = measure['name']
        self.steward = measure['steward']
        self.properties = {property: Property(value['name'], value['type'], value['codes']) for property, value in measure['properties'].items()}
        if any(param not in params for param in measure['parameters']):
            raise Exception("No value supplied for measure parameter")
        self.parameters = {param: Parameter(value['name'], value['type'], params[param]) for param, value in measure['parameters'].items()}
        parser = Operator(self.parameters)
        self.parameters.update({param: parser.parse(value) for param, value in measure['calculated_dates'].items()})


class Property:
    def __init__(self, name, type, codes):
        self.name = name
        self.type = SUPPORTED_PROPERTY_TYPES.get_type(type)
        self.codes = codes


class Parameter:
    def __init__(self, name, type, value):
        self.name = name
        self.type = SUPPORTED_PROPERTY_TYPES.get_type(type)
        self.value = value


class Operator:
    def __init__(self, parameters):
        self.parameters = parameters


class Minus(Operator):
    def __init__(self, parameters, operands):
        super().__init__(parameters)
        if len(operands) != 2:
            raise Exception("Number of operands must be 2, {} supplied".format(len(operands)))


class TimePeriod:
    SECONDS_IN_A_YEAR = 365*24*60*60
    UNIT_FACTOR = {'year': SECONDS_IN_A_YEAR, 'month': SECONDS_IN_A_YEAR/12, 'day': 24*60*60, 'second': 1}

    def __init__(self, parameters, hash):
        super().__init__(parameters)
        self.value = int(hash['val'])
        self.unit = hash['unit']
        if self.unit not in self.UNIT_FACTOR:
            raise Exception(f"Unknown unit: {self.unit}")

    def evaluate(self):
        return self.value * self.UNIT_FACTOR[self.unit]
