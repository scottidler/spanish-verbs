#!/bin/env python3

import sys
import jsonschema
import argparse
from ruamel.yaml import YAML

yaml = YAML(typ='safe', pure=True)

def validate_conjugation_file(conjugation_file_path, schema_file_path):
    try:
        # Load the YAML file containing verb conjugations
        with open(conjugation_file_path, 'r', encoding='utf-8') as file:
            conjugation_data = yaml.load(file)

        # Load the JSON schema
        with open(schema_file_path, 'r', encoding='utf-8') as schema_file:
            schema = yaml.load(schema_file)

        # Validate the conjugation data against the schema
        jsonschema.validate(conjugation_data, schema)
        return True
    except Exception as e:
        #print(f"Validation error: {e}", file=sys.stderr)
        print(f"Validation error: {e}")
        return False

def main(args):
    parser = argparse.ArgumentParser(description="Validate conjugation files against a JSON schema")
    parser.add_argument("verbs", metavar='VERB', nargs='+', help="Path(s) to the conjugation YAML file(s)")
    parser.add_argument("-s", "--schema", metavar='FILE', default='verb-schema.yml', help="Path to the JSON schema file")

    args = parser.parse_args(args)

    for verb_file in args.verbs:
        if validate_conjugation_file(verb_file, args.schema):
            print(f"Validation successful for {verb_file}")
        else:
            print(f"Validation failed for {verb_file}")

if __name__ == "__main__":
    main(sys.argv[1:])

