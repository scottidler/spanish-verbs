#!/bin/env python3

import sys
import os
import json
import openai
import argparse

from ruamel.yaml import YAML
from jsonschema import validate, ValidationError

yaml = YAML(typ='safe')
yaml.default_flow_style = False  # Set flow style to block (more human-readable)

def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        return yaml.load(file)

def validate_conjugation(conjugation, schema):
    try:
        validate(instance=conjugation, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return False

def get_conjugation(verb, api_key, example_yaml, schema):
    prompt = (
        f'Conjugate the Spanish verb "{verb}" in all 14 tenses and moods, as well as the infinitive, gerundio and past participle.\n\n'
        f'{example_yaml}\n\n'
        'Here is the schema that will be used to validate your response via jsconschema.\n\n'
        f'{schema}\n\n'
        'Your response should be in yaml. You most conform to all of the field names you see in the example above.'
        f'The only field that will differ is the name of the verb which should match my query: {verb}'
        'Make sure you provide ALL 17 top-level fields as specified in the example yaml and the schema.'
        "In previous queries: Validation error: 'infinitivo' is a required property."
    )

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message['content']
        conjugation_data = response_text.strip()
        conjugation = yaml.load(conjugation_data)
        if validate_conjugation(conjugation, schema):
            return conjugation
    except Exception as e:
        print(f"Error in getting or processing response: {e}", file=sys.stderr)

    return None

def main(args):
    parser = argparse.ArgumentParser(description='Get verb conjugations using ChatGPT API.')
    parser.add_argument('verbs', nargs='+', help='List of infinitive verbs')
    args = parser.parse_args(args)

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        sys.stderr.write('Error: OPENAI_API_KEY environment variable not set.\n')
        return

    schema = load_schema('verb-schema.yml')

    try:
        with open('hablar.yml', 'r') as file:
            example_yaml = file.read()
    except FileNotFoundError:
        sys.stderr.write('Example file \'hablar.yml\' not found. Please provide an example YAML file.\n')
        return

    for verb in args.verbs:
        conjugations = get_conjugation(verb, api_key, example_yaml, schema)
        if conjugations:
            file_name = f'{verb}.yml'
            with open(file_name, 'w') as file:
                yaml.dump(conjugations, file)
            sys.stdout.write(f'Conjugations for \'{verb}\' successfully saved to {file_name}\n')
        else:
            sys.stderr.write(f'Failed to get valid conjugations for \'{verb}\'\n')

if __name__ == '__main__':
    main(sys.argv[1:])

