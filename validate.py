#!/bin/env python3

import os
import sys
import requests
import argparse
from pathlib import Path

MWD_API_KEY = os.environ.get('MWD_API_KEY')

def is_valid_spanish_verb(verb, api_key):
    url = f'https://dictionaryapi.com/api/v3/references/spanish/json/{verb}?key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return bool(data and 'shortDef' in data[0])
    return False

def rename_invalid_files(directory):
    for file in Path(directory).glob('*.yml'):
        verb = file.stem
        if not is_valid_spanish_verb(verb, MWD_API_KEY):
            new_filename = file.with_suffix('.yml.to-be-deleted')
            file.rename(new_filename)
            print(f"Renamed invalid verb file: {file} -> {new_filename}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Validate and rename Spanish verb YAML files.')
    parser.add_argument('-d', '--directory', default='verbs', help='Directory containing .yml files')
    return parser.parse_args()

def main():
    args = parse_arguments()
    if not MWD_API_KEY:
        print('Error: MWD_API_KEY environment variable not set.', file=sys.stderr)
        sys.exit(1)
    rename_invalid_files(args.directory)

if __name__ == '__main__':
    main()

