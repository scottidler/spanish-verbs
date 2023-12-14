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
        return True, None
    except ValidationError as e:
        return False, e.message
    except Exception as e:
        return False, f'YAML parsing error: {e}'

def get_conjugation(verb, prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logger.error(f'Error "{verb}": {e}')
        return None

def get_corrected_conjugation(verb, original_prompt, error_message):
    correction_prompt = (
        f'Original task for "{verb}":\n{original_prompt}\n\n'
        f'Validation Error: {error_message}\n\n'
        f'Please provide a corrected version of the conjugation for "{verb}", '
        'ensuring it conforms to the schema requirements.'
    )
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': correction_prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logger.error(f'Error in correction attempt for "{verb}": {e}')
        return None

def tab_in_content(content, spaces=2):
    return ''.join(' ' * spaces + line if line.strip() else line for line in content)

def main(args):
    parser = argparse.ArgumentParser(description='Get verb conjugations using ChatGPT API.')
    parser.add_argument('verbs', nargs='+', help='List of infinitive verbs')
    parser.add_argument('-o', '--output', default='verbs', help='Output directory (default: verbs)')
    parser.add_argument('-p', '--prompt-only', action='store_true', help='Print prompt only and exit')
    parser.add_argument('-f', '--force', action='store_true', help='Force re-conjugation and file rewrite')
    ns = parser.parse_args(args)

    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    else:
        sys.stderr.write('Error: OPENAI_API_KEY environment variable not set.\n')
        sys.exit(1)

    try:
        with open(f'{ns.output}/hablar.yml', 'r') as file:
            example_yaml = tab_in_content(file, 2)
    except FileNotFoundError:
        sys.stderr.write("Example file 'hablar.yml' not found. Please provide an example YAML file.\n")
        return

    with open('schema.yml', 'r') as schema_file:
        schema_content = tab_in_content(schema_file, 2)

    schema_yaml = load_schema('schema.yml')

    output_dir = ns.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = len(ns.verbs)
    for index, verb in enumerate(ns.verbs, start=1):
        percentage = round((index / count) * 100)
        prefix = f'{index}/{count} ({percentage}%)'
        file_path = os.path.join(output_dir, f'{verb}.yml')

        if not ns.force and os.path.exists(file_path):
            logger.info(f'Existing "{verb}": {file_path}')
            continue

        prompt = (
            f'Conjugate the Spanish verb "{verb}" in all 14 tenses and moods, '
            'as well as the infinitive, gerundio and past participle.\n\n'
            f'Follow this example:\n{example_yaml}\n\n'
            f'Validation will use this schema:\n{schema_content}\n\n'
            'Your response should be in YAML format and conform to the field names '
            'and structure specified in the schema above.'
        )

        if ns.prompt_only:
            print(prompt)
            continue

        try:
            conjugation_yaml = get_conjugation(verb, prompt)
            is_valid, error_message = validate_conjugation(conjugation_yaml, schema_yaml)
            if is_valid:
                with open(file_path, 'w') as file:
                    file.write(conjugation_yaml)
                logger.info(f'Created "{verb}" -> {file_path}')
            else:
                logger.error(f'Validation error for "{verb}": {error_message}')
                corrected_yaml = get_corrected_conjugation(verb, prompt, error_message)
                is_corrected_valid, corrected_error_message = validate_conjugation(corrected_yaml, schema_yaml)
                if is_corrected_valid:
                    with open(file_path, 'w') as file:
                        file.write(corrected_yaml)
                    logger.info(f'Corrected and created "{verb}" -> {file_path}')
                else:
                    logger.error(f'Failed to correct "{verb}"')
        except Exception as e:
            sys.stderr.write(f'Error processing "{verb}": {e}\n')

if __name__ == '__main__':
    main(sys.argv[1:])

