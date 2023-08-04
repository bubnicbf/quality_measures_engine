import json
import unittest
from JSONDocumentBuilder import JSONDocumentBuilder

class TestJSONDocumentBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
            cls.measure_json = json.load(f)
        with open('fixtures/complex_measure.json') as f:
            cls.complex_measure_json = json.load(f)

    def test_calculate_dates(self):
        jdb = JSONDocumentBuilder(self.measure_json)
        jdb.parameters = {'effective_date': 1287685441}
        jdb.calculate_dates()
        self.assertEqual(jdb.calculated_dates['earliest_birthdate'], -762154559)

    def test_create_query_simple_measure(self):
        jdb = JSONDocumentBuilder(self.measure_json, {'effective_date': 1287685441})
        query_hash = jdb.create_query(self.measure_json['denominator'])
        self.assertEqual(len(query_hash), 1)
        self.assertIsNotNone(query_hash.get('measures.0043.encounter'))
        self.assertEqual(query_hash['measures.0043.encounter']['$gte'], 1256149441)

    def test_transform_property_name(self):
        jdb = JSONDocumentBuilder(self.measure_json, {'effective_date': 1287685441})
        self.assertEqual(jdb.transform_query_property('birthdate'), 'birthdate')
        self.assertEqual(jdb.transform_query_property('foo'), 'measures.0043.foo')

    def test_process_query_leaf_expression(self):
        jdb = JSONDocumentBuilder(self.measure_json, {'effective_date': 1287685441})
        args = {}
        jdb.process_query({"encounter": {"_gte": "@earliest_encounter"}}, args)
        self.assertEqual(len(args), 1)
        self.assertIsNotNone(args.get('measures.0043.encounter'))
        self.assertEqual(args['measures.0043.encounter']['$gte'], 1256149441)

    def test_process_query_leaf_value(self):
        jdb = JSONDocumentBuilder(self.measure_json, {'effective_date': 1287685441})
        args = {}
        jdb.process_query({"encounter": 'splat'}, args)
        self.assertEqual(len(args), 1)
        self.assertIsNotNone(args.get('measures.0043.encounter'))
        self.assertEqual(args['measures.0043.encounter'], 'splat')

    def test_create_query_complex_measure(self):
        jdb = JSONDocumentBuilder(self.complex_measure_json)
        query_hash = jdb.create_query(self.complex_measure_json['population'])
        self.assertEqual(query_hash['measures.0043.age']['$gt'], 17)
        self.assertEqual(query_hash['measures.0043.age']['$lt'], 75)
        self.assertEqual(len(query_hash['$or']), 2)

if __name__ == '__main__':
    unittest.main()
