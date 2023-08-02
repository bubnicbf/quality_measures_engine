import json
import unittest
import time
from measure import Measure, UnsupportedPropertyTypeError, NoValueSuppliedForMeasureParameterError

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

class TestMeasure(unittest.TestCase):
    def setUp(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
            self.measure_json = f.read()
        self.hash = json.loads(self.measure_json)

    def test_metadata_extraction(self):
        measure = Measure(self.hash, {'effective_date': int(time.time())})
        self.assertEqual(measure.id, '0043')
        self.assertEqual(measure.name, 'Pneumonia Vaccination Status for Older Adults')
        self.assertEqual(measure.steward, 'NCQA')

    def test_property_extraction(self):
        measure = Measure(self.hash, {'effective_date': int(time.time())})
        self.assertEqual(len(measure.properties), 3)
        self.assertIn('birthdate', measure.properties)
        self.assertIn('encounter', measure.properties)
        self.assertIn('vaccination', measure.properties)
        # Repeat for all property types and codes as needed...

    def test_parameter_extraction(self):
        time_now = int(time.time())
        measure = Measure(self.hash, {'effective_date': time_now})
        self.assertEqual(len(measure.parameters), 3)
        self.assertIn('effective_date', measure.parameters)
        self.assertEqual(measure.parameters['effective_date'].type, 'long')
        self.assertEqual(measure.parameters['effective_date'].value, time_now)

    def test_invalid_measure(self):
        invalid_hash = json.loads(invalid_measure_json)
        with self.assertRaises(UnsupportedPropertyTypeError):
            Measure(invalid_hash, {'effective_date': int(time.time())})

    def test_no_parameters(self):
        with self.assertRaises(NoValueSuppliedForMeasureParameterError):
            Measure(self.hash)

    def test_calculated_dates(self):
        date = int(time.time())
        measure = Measure(self.hash, {'effective_date': date})
        self.assertEqual(measure.parameters['earliest_encounter'].value, date-365*24*60*60)

if __name__ == '__main__':
    unittest.main()
