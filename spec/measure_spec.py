import unittest
import json
import time
from measure import Measure, UnsupportedPropertyTypeError

invalid_measure_json = """
{
  "id": "0043",
  "name": "Pneumonia Vaccination Status for Older Adults",
  "steward": "NCQA",
  "parameters": {
    "effective_date": {
      "name": "Effective end date for measure",
      "type": "long"
    }
  },
  "properties": {
    "birthdate": {
      "name": "Date of birth",
      "type": "invalid_type",
      "codes": {
        "HL7": {
          "3.0": ["00110"]
        }
      }
    }
  }
}
"""

class TestEngineMeasure(unittest.TestCase):
    def setUp(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json', 'r') as f:
            self.measure_json = json.load(f)
            self.time = int(time.time())
            self.measure = Measure(self.measure_json, {'effective_date': self.time})

    def test_should_extract_the_measure_metadata(self):
        self.assertEqual(self.measure.id, '0043')
        self.assertEqual(self.measure.name, 'Pneumonia Vaccination Status for Older Adults')
        self.assertEqual(self.measure.steward, 'NCQA')

    def test_should_extract_three_properties_for_measure_0043(self):
        self.assertEqual(len(self.measure.properties), 3)
        self.assertIn('birthdate', self.measure.properties)
        self.assertIn('encounter', self.measure.properties)
        self.assertIn('vaccination', self.measure.properties)
        self.assertEqual(self.measure.properties['birthdate'].type, 'long')
        self.assertEqual(len(self.measure.properties['birthdate'].codes), 1)
        self.assertIn('HL7', self.measure.properties['birthdate'].codes)
        self.assertEqual(self.measure.properties['encounter'].type, 'long')
        self.assertEqual(len(self.measure.properties['encounter'].codes), 2)
        self.assertIn('CPT', self.measure.properties['encounter'].codes)
        self.assertIn('ICD-9-CM', self.measure.properties['encounter'].codes)
        self.assertEqual(self.measure.properties['vaccination'].type, 'boolean')

    def test_should_extract_three_parameters_for_measure_0043(self):
        self.assertEqual(len(self.measure.parameters), 3)
        self.assertIn('effective_date', self.measure.parameters)
        self.assertEqual(self.measure.parameters['effective_date'].type, 'long')
        self.assertEqual(self.measure.parameters['effective_date'].value, self.time)

    def test_should_raise_a_RuntimeError_for_invalid_measures(self):
        hash = json.loads(invalid_measure_json)
        with self.assertRaises(UnsupportedPropertyTypeError):
            Measure(hash, {'effective_date': int(time.time())})

    def test_should_raise_a_RuntimeError_if_not_passed_all_the_parameters(self):
        with self.assertRaises(Exception):
            Measure(self.measure_json)

    def test_should_calculate_the_calculated_dates_correctly(self):
        self.assertEqual(self.measure.parameters['earliest_encounter'].value, self.time - Measure.YEAR_IN_SECONDS)


if __name__ == '__main__':
    unittest.main()
