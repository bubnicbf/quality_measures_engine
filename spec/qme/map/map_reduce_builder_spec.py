import unittest
import json
import time
from your_module import Measure, Builder  # Replace 'your_module' with the actual module name

class TestBuilder(unittest.TestCase):
    def test_javascript_expressions(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json', 'r') as f:
            measure_json = f.read()
        data = json.loads(measure_json)
        date = int(time.time())
        measure = Measure(data, {'effective_date': date})
        builder = Builder(data, {'effective_date': date})
        self.assertEqual(builder.numerator(), 'measures.0043.vaccination==true')
        self.assertEqual(builder.denominator(), f'measures.0043.encounter>={measure.parameters["earliest_encounter"].value}')
        self.assertEqual(builder.population(), f'measures.0043.birthdate<={measure.parameters["earliest_birthdate"].value}')
        self.assertEqual(builder.exception(), '')

if __name__ == "__main__":
    unittest.main()
