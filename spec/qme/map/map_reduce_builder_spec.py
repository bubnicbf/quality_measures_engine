import json
import unittest
from time import gmtime, mktime
from Builder import Builder

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
    @classmethod
    def setUpClass(cls):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json', 'r') as f:
            cls.measure_json = json.load(f)
        with open('fixtures/complex_measure.json', 'r') as f:
            cls.complex_measure_json = json.load(f)

    def test_should_extract_the_measure_metadata(self):
        measure = Builder(self.measure_json, {'effective_date': int(mktime(gmtime(2010, 9, 19)))})
        self.assertEqual(measure.id, '0043')

    def test_should_extract_three_parameters_for_measure_0043(self):
        time = int(mktime(gmtime(2010, 9, 19)))
        measure = Builder(self.measure_json, {'effective_date': time})
        self.assertEqual(len(measure.parameters), 3)
        self.assertIn('effective_date', measure.parameters)
        self.assertEqual(measure.parameters['effective_date'], time)

    def test_should_raise_RuntimeError_if_not_passed_all_the_parameters(self):
        with self.assertRaises(RuntimeError, msg='No value supplied for measure parameter: effective_date'):
            Builder(self.measure_json)

    def test_should_calculate_the_calculated_dates_correctly(self):
        date = int(mktime(gmtime(2010, 9, 19)))
        measure = Builder(self.measure_json, {'effective_date': date})
        self.assertEqual(measure.parameters['earliest_encounter'], date - Builder.YEAR_IN_SECONDS)

    def test_should_produce_valid_JavaScript_expressions_for_the_query_components(self):
        date = int(mktime(gmtime(2010, 9, 19)))
        builder = Builder(self.measure_json, {'effective_date': date})
        self.assertEqual(builder.numerator, '(this.measures["0043"].vaccination==true)')
        self.assertEqual(builder.denominator, '(this.measures["0043"].encounter>=' + str(builder.parameters['earliest_encounter']) + ')')
        self.assertEqual(builder.population, '(this.birthdate<=' + str(builder.parameters['earliest_birthdate']) + ')')
        self.assertEqual(builder.exception, '(false)')
        self.assertEqual(builder.map_function, MAP_FUNCTION)
        self.assertEqual(builder.reduce_function, Builder.REDUCE_FUNCTION)

    def test_should_handle_logical_combinations(self):
        builder = Builder(self.complex_measure_json, {})
        self.assertEqual(builder.population, '((this.measures["0043"].age>17)&&(this.measures["0043"].age<75)&&((this.measures["0043"].sex=="male")||(this.measures["0043"].sex=="female")))')

if __name__ == '__main__':
    unittest.main()
