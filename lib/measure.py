import json
import unittest

# assuming the classes TimePeriod, Minus, Operator are defined in the file measure.py
from measure import TimePeriod, Minus, Operator

class TestTimePeriod(unittest.TestCase):
    def test_extract_value_and_units_from_a_hash(self):
        period_json = '{"val": "1", "unit":"year"}'
        hash = json.loads(period_json)
        period = TimePeriod({}, hash)
        self.assertEqual(period.evaluate(), 365*24*60*60)

class TestMinus(unittest.TestCase):
    def test_support_two_val_unit_args(self):
        args_json = '[{"val": "1", "unit":"year"}, {"val": "1", "unit":"year"}]'
        arr = json.loads(args_json)
        minus = Minus({}, arr)
        self.assertEqual(minus.evaluate(), 0)
        
    def test_support_one_val_unit_arg_and_one_reference(self):
        args_json = '["@param", {"val": "2", "unit":"second"}]'
        arr = json.loads(args_json)
        minus = Minus({"param": 4}, arr)
        self.assertEqual(minus.evaluate(), 2)
        
    def test_support_one_val_unit_arg_and_one_explicit_number(self):
        args_json = '["4", {"val": "2", "unit":"second"}]'
        arr = json.loads(args_json)
        minus = Minus({"param": 2}, arr)
        self.assertEqual(minus.evaluate(), 2)

class TestOperator(unittest.TestCase):
    def test_be_able_to_perform_minus_on_years(self):
        args_json = '{"$minus": [{"val": "1", "unit":"year"}, {"val": "1", "unit":"year"}]}'
        arr = json.loads(args_json)
        minus = Operator({}).parse(arr)
        self.assertEqual(minus.evaluate(), 0)
        
    def test_be_able_to_perform_minus_on_seconds(self):
        args_json = '{"$minus": [{"val": "3", "unit":"second"}, {"val": "1", "unit":"second"}]}'
        arr = json.loads(args_json)
        minus = Operator({}).parse(arr)
        self.assertEqual(minus.evaluate(), 2)

if __name__ == '__main__':
    unittest.main()
