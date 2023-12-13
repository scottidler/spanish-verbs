#!/bin/env python3

import os
import sys
import openai
import argparse
from ruamel.yaml import YAML
from jsonschema import validate, ValidationError
import logging

yaml = YAML(typ='safe')
yaml.default_flow_style = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        return yaml.load(file)

def validate_conjugation(conjugation_yaml, schema):
    try:
        conjugation = yaml.load(conjugation_yaml)
        validate(instance=conjugation, schema=schema)
        return True
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return False

def get_conjugation(verb, prompt):

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message['content']
        return content.strip()
    except Exception as e:
        logger.error(f"Error in getting or processing response: {e}")
        return None

def main(args):
    parser = argparse.ArgumentParser(description='Get verb conjugations using ChatGPT API.')
    parser.add_argument('verbs', nargs='+', help='List of infinitive verbs')
    parser.add_argument('-o', '--output', default='verbs', help='Output directory (default: verbs)')
    parser.add_argument('-p', '--prompt-only', action='store_true', help='Print prompt only and exit')
    parser.add_argument('-f', '--force', action='store_true', help='Force re-conjugation and file rewrite')
    ns = parser.parse_args(args)

    schema_yaml = load_schema('verb-schema.yml')

    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    else:
        sys.stderr.write('Error: OPENAI_API_KEY environment variable not set.\n')
        sys.exit(1)

    try:
        with open(f'{ns.output}/hablar.yml', 'r') as file:
            example_yaml = file.read()
    except FileNotFoundError:
        sys.stderr.write('Example file \'hablar.yml\' not found. Please provide an example YAML file.\n')
        return

    output_dir = ns.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for verb in ns.verbs:
        file_path = os.path.join(output_dir, f'{verb}.yml')

        if not ns.force and os.path.exists(file_path):
            logger.info(f'Conjugations for \'{verb}\' already exist. Use -f or --force to re-conjugate.')
            continue

        prompt = (
            f'Conjugate the Spanish verb "{verb}" in all 14 tenses and moods, as well as the infinitive, gerundio and past participle.\n\n'
            f'{example_yaml}\n\n'
            'Here is the schema that will be used to validate your response via jsonschema.\n\n'
            f'{schema_yaml}\n\n'
            'Your response should be in yaml. You must conform to all of the field names you see in the example above.'
            f'The only field that will differ is the name of the verb which should match my query: {verb}'
            'Make sure you provide ALL 17 top-level fields as specified in the example yaml and the schema.'
        )

        if ns.prompt_only:
            print(prompt)
            print()
        else:
            conjugation_yaml = get_conjugation(verb, prompt)
            if conjugation_yaml and validate_conjugation(conjugation_yaml, schema_yaml):
                with open(file_path, 'w') as file:
                    file.write(conjugation_yaml)
                logger.info(f'Conjugations for \'{verb}\' successfully saved to {file_path}')
            else:
                logger.error(f'Failed to get valid conjugations for \'{verb}\'')

if __name__ == '__main__':
    main(sys.argv[1:])

