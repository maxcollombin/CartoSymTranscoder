import json
from jsonschema import validate, ValidationError, Draft7Validator
from jsonschema.exceptions import best_match

# Load the schema
with open('CartoSym-JSON.schema.json', 'r') as f:
    schema = json.load(f)

# Load the JSON file
with open('../examples/1-core.cs.json', 'r') as f:
    data = json.load(f)

# Create a validator
validator = Draft7Validator(schema)

# Validate the JSON data
errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
if errors:
    for error in errors:
        print(error.message)
else:
    print("JSON data is valid")