from py_mini_racer import py_mini_racer

class JSONDocumentBuilder:
    def __init__(self, measure_json, parameters=None):
        self.measure_json = measure_json
        self.parameters = parameters if parameters else {}
        self.calculated_dates = {}

        if self.parameters:
            self.calculate_dates()

    def calculate_dates(self):
        ctx = py_mini_racer.MiniRacer()

        for key, value in self.parameters.items():
            ctx.eval(f'{key} = {value}')

        # TODO: Replace this with a js file that has all constants
        ctx.eval('year = 365 * 24 * 60 * 60')

        self.calculated_dates = {}
        for key, value in self.measure_json["calculated_dates"].items():
            self.calculated_dates[key] = ctx.eval(value)
