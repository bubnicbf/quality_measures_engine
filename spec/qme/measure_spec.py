import json
import time
from measure import Measure

def test_measure():
    with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
        measure_json = json.load(f)

    date = time.mktime(time.strptime('2010-09-19', '%Y-%m-%d'))
    measure = Measure(measure_json, {"effective_date": date})

    assert measure.id == '0043'
    assert measure.name == 'Pneumonia Vaccination Status for Older Adults'
    assert measure.steward == 'NCQA'

def test_parameters():
    with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
        measure_json = json.load(f)

    date = time.mktime(time.strptime('2010-09-19', '%Y-%m-%d'))

    measure = Measure(measure_json, {"effective_date": date})
    assert len(measure.parameters) == 3
    assert "effective_date" in measure.parameters
    assert measure.parameters["effective_date"] == date

def test_missing_parameters():
    with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
        measure_json = json.load(f)

    try:
        Measure(measure_json, {})
        assert False, "Expected an error due to missing parameters"
    except RuntimeError as e:
        assert str(e) == 'No value supplied for measure parameter: effective_date'

def test_calculated_dates():
    with open('measures/0043/0043_NQF_PneumoniaVaccinationStatusForOlderAdults.json') as f:
        measure_json = json.load(f)

    date = time.mktime(time.strptime('2010-09-19', '%Y-%m-%d'))

    measure = Measure(measure_json, {"effective_date": date})
    assert measure.parameters["earliest_encounter"] == date - Measure.YEAR_IN_SECONDS
