import json
import unittest
import time
from measure import Measure, Builder

complex_measure_json = """
{
  "id": "0043",
  "name": "Pneumonia Vaccination Status for Older Adults",
  "steward": "NCQA",
  "population": {
    "$and": [
      {
        "category": "Patient Characteristic",
        "title": "Age > 17 before measure period",
        "query": {"age": {"$gt": 17}}
      },
      {
        "category": "Patient Characteristic",
        "title": "Age < 75 before measure period",
        "query": {"age": {"$lt": 75}}
      },
      {
        "$or": [
          {
            "category": "Patient Characteristic",
            "title": "Male",
            "query": {"sex": "male"}
          },
          {
            "category": "Patient Characteristic",
            "title": "Female",
            "query": {"sex": "female"}
          }
        ]
      }
    ]
  },
  "denominator": {},
  "numerator": {},
  "exception": {}
}
"""

class TestBuilder(unittest.TestCase):
    def test_valid_JavaScript_expressions(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json', 'r') as f:
            measure_json = f.read()
        hash = json.loads(measure_json)
        date = int(time.time())
        measure = Measure(hash, {'effective_date': date})
        builder = Builder(hash, {'effective_date': date})
        self.assertEqual(builder.numerator(), '(measures["0043"].vaccination==true)')
        self.assertEqual(builder.denominator(), f'(measures["0043"].encounter>={measure.parameters["earliest_encounter"].value})')
        self.assertEqual(builder.population(), f'(measures["0043"].birthdate<={measure.parameters["earliest_birthdate"].value})')
        self.assertEqual(builder.exception(), '(false)')

    def test_handle_logical_combinations(self):
        hash = json.loads(complex_measure_json)
        measure = Measure(hash, {})
        builder = Builder(hash, {})
        self.assertEqual(builder.population(), '((measures["0043"].age>17)&&(measures["0043"].age<75)&&((measures["0043"].sex=="male")||(measures["0043"].sex=="female")))')

if __name__ == '__main__':
    unittest.main()
