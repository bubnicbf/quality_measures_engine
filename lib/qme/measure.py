import json
from PyV8 import JSContext
from typing import Any, Dict

class Measure:
    YEAR_IN_SECONDS = 365*24*60*60
    
    def __init__(self, measure: Dict[str, Any], params: Dict[str, Any]):
        self.id = measure['id']
        self.name = measure['name']
        self.steward = measure['steward']
        self.parameters = {}
        measure['parameters'] = measure.get('parameters', {})

        for parameter, value in measure['parameters'].items():
            if parameter not in params:
                raise ValueError(f"No value supplied for measure parameter: {parameter}")
            self.parameters[parameter] = params[parameter]

        ctx = JSContext()
        ctx['year'] = self.YEAR_IN_SECONDS
        for key, param in self.parameters.items():
            ctx[key] = param

        measure['calculated_dates'] = measure.get('calculated_dates', {})
        for parameter, value in measure['calculated_dates'].items():
            self.parameters[parameter] = ctx.eval(value)
