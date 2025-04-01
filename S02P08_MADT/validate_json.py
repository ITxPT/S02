import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import os



def validate_json(data, schema):
    try:
        schema_resource = DRAFT202012.create_resource(schema)
        registry = Registry().with_resource(uri="urn:schema", resource=schema_resource)
        
        # Use the registry to validate the instance
        validator = Draft202012Validator(schema=schema, registry=registry)
        validator.validate(data)

        #print("Valid JSON!")
        return True
    except ValidationError as e:
        print(f"Invalid JSON: {e}")
        print("Failed at: ", e.absolute_path)  # Shows the path in the data where the validation failed
        print("Schema path: ", e.schema_path)  # Shows the path in the schema that triggered the error
        return False

def load_json(schema_path):
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return schema

# Get schema and data from folders
json_examples = [f for f in os.listdir('examples') if f.endswith('.json')]
json_schemas = [f for f in os.listdir('json schemas') if f.endswith('.json')]

# Pair JSON examples and schemas based on filenames
paired_files = {}
for example in json_examples:
    base_name = os.path.splitext(example)[0]
    schema_file = f"{base_name}.json"
    if schema_file in json_schemas:
        paired_files[base_name] = (os.path.join('examples', example), os.path.join('json schemas', schema_file))

# Validate the JSON examples
for base_name, (example_path, schema_path) in paired_files.items():
    print(f"Validating {example_path}...")
    example_data = load_json(example_path)
    schema = load_json(schema_path)
    if validate_json(example_data, schema):
        print("Valid JSON")
    else:
        print("Invalid JSON!!!")