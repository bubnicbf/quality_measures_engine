import json
import unittest
from measure import Measure
from datetime import datetime
import time

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
    def test_measure_metadata(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
            measure_json = f.read()
        hash = json.loads(measure_json)
        measure = Measure(hash, {'effective_date': int(time.mktime(datetime.now().timetuple()))})
        self.assertEqual(measure.id, '0043')
        self.assertEqual(measure.name, 'Pneumonia Vaccination Status for Older Adults')
        self.assertEqual(measure.steward, 'NCQA')

    def test_extract_properties(self):
        # Add assertions similar to 'test_measure_metadata' method

    def test_extract_parameter(self):
        # Add assertions similar to 'test_measure_metadata' method

    def test_runtime_error_invalid_measures(self):
        hash = json.loads(invalid_measure_json)
        with self.assertRaises(Exception) as context:
            measure = Measure(hash, {'effective_date': int(time.mktime(datetime.now().timetuple()))})
        self.assertTrue('Unsupported property type: invalid_type' in str(context.exception))

    def test_runtime_error_no_value_parameter(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
            measure_json = f.read()
        hash = json.loads(measure_json)
        with self.assertRaises(Exception) as context:
            measure = Measure(hash)
        self.assertTrue('No value supplied for measure parameter: effective_date' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
