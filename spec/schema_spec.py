import json
import glob
from jsonschema import validate, ValidationError
import unittest

class TestJSONSchemas(unittest.TestCase):
    def test_conform_to_json_schema(self):
        with open("schema/schema.json", 'r') as f:
            schema = json.load(f)

        for schema_file in glob.glob('schema/*.json'):
            if schema_file != 'schema/schema.json':  # Don't check the schema itself
                with open(schema_file, 'r') as f:
                    data = json.load(f)
                try:
                    validate(instance=data, schema=schema)
                except ValidationError as v:
                    self.fail(f"JSON data in {schema_file} did not validate against the schema: {v}")

if __name__ == '__main__':
    unittest.main()
