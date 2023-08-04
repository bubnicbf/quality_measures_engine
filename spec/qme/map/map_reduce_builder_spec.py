import unittest
import json
import time
from Measure import Builder

COMPLEX_MEASURE_JSON = """
{
  "id": "0043",
  "name": "Pneumonia Vaccination Status for Older Adults",
  "steward": "NCQA",
  "population": {
    "and": [
      {
        "category": "Patient Characteristic",
        "title": "Age > 17 before measure period",
        "query": {"age": {"_gt": 17}}
      },
      {
        "category": "Patient Characteristic",
        "title": "Age < 75 before measure period",
        "query": {"age": {"_lt": 75}}
      },
      {
        "or": [
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

MAP_FUNCTION = """
function () {
  var value = {i: 0, d: 0, n: 0, e: 0};
  if (this.birthdate<=-764985600) {
    value.i++;
    if (this.measures["0043"].encounter>=1253318400) {
      value.d++;
      if (this.measures["0043"].vaccination==true) {
        value.n++;
      } else if (false) {
        value.e++;
        value.d--;
      }
    }
  }
  emit(null, value);
};
"""

class TestBuilder(unittest.TestCase):
    def setUp(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
            self.measure_json = json.load(f)
        self.time = time.mktime(time.strptime("19/09/2010", "%d/%m/%Y"))

    def test_measure_metadata(self):
        measure = Builder(self.measure_json, {'effective_date': self.time})
        self.assertEqual(measure.id, '0043')

    def test_extract_three_parameters(self):
        measure = Builder(self.measure_json, {'effective_date': self.time})
        self.assertEqual(len(measure.parameters), 3)
        self.assertIn('effective_date', measure.parameters)
        self.assertEqual(measure.parameters['effective_date'], self.time)

    def test_raise_error_on_missing_parameter(self):
        with self.assertRaises(RuntimeError):
            Builder(self.measure_json)

    def test_calculate_dates_correctly(self):
        measure = Builder(self.measure_json, {'effective_date': self.time})
        self.assertEqual(measure.parameters['earliest_encounter'], self.time - Builder.YEAR_IN_SECONDS)

    # Add more tests here...
