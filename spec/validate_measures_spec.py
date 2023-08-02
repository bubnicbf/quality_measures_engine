import pytest
import json
import glob
import os

def test_all_measure_specifications_are_valid_json():
    for measure_file in glob.glob('measures/*/*.json'):
        with open(measure_file, 'r') as f:
            measure = f.read()
        try:
            json.loads(measure)
        except json.JSONDecodeError:
            pytest.fail(f"File {measure_file} is not valid JSON")

def test_all_patient_samples_are_valid_json():
    for measure_file in glob.glob('measures/*/patients/*.json'):
        with open(measure_file, 'r') as f:
            measure = f.read()
        try:
            json.loads(measure)
        except json.JSONDecodeError:
            pytest.fail(f"File {measure_file} is not valid JSON")
