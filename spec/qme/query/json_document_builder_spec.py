import json
import pytest
from JSONDocumentBuilder import JSONDocumentBuilder

class TestJSONDocumentBuilder:

    @pytest.fixture(autouse=True)
    def prepare(self):
        with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json', 'r') as file:
            raw_measure_json = file.read()
        self.measure_json = json.loads(raw_measure_json)

    def test_calculate_dates(self):
        jdb = JSONDocumentBuilder(self.measure_json)
        jdb.parameters = {'effective_date': 1287685441}
        jdb.calculate_dates()
        assert jdb.calculated_dates['earliest_birthdate'] == -762154559
