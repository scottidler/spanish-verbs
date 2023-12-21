#!/bin/env python3

import os
import sys
import argparse
import genanki
import time
import yaml

def load_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_anki_cloze_card(text, cloze_number, model):
    return genanki.Note(
        model=model,
        fields=[text, str(cloze_number)]
    )

def process_yaml_file(file_path, deck, model):
    data = load_yaml_file(file_path)
    meaning = data.get('meaning')
    infinitive = data.get('infinitivo')

    if meaning is None or infinitive is None:
        print(f"Error in file {file_path}: Missing 'meaning' or 'infinitivo'", file=sys.stderr)
        return

    cloze_text = f"{infinitive} ({{{{c1::{meaning}}}}})"
    deck.add_note(create_anki_cloze_card(cloze_text, 1, model))


def process_directory(path, deck, model):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.yml'):
                process_yaml_file(os.path.join(root, file), deck, model)

def main(args):
    deck_id = int(time.time())
    deck = genanki.Deck(deck_id, args.deck_name)

    model = genanki.Model(
        int(time.time() * 1000),
        'Cloze Model',
        fields=[
            {'name': 'Text'},
            {'name': 'Cloze'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{cloze:Text}}',
                'afmt': '{{cloze:Text}}',
            },
        ],
        model_type=genanki.Model.CLOZE
    )

    for item in args.paths:
        if os.path.isdir(item):
            process_directory(item, deck, model)
        elif os.path.isfile(item):
            process_yaml_file(item, deck, model)

    deck.write_to_file(args.output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Anki cards from YAML files")
    parser.add_argument(
        'paths',
        metavar='[FILE..]',
        nargs='+',
        help='Paths to YAML files or directories containing YAML files')
    parser.add_argument(
        '-n',
        '--deck-name',
        metavar='NAME',
        default='Spanish Infinitives',
        help='Name of the Anki deck')
    parser.add_argument(
        '-f',
        '--output-file',
        metavar='FILE',
        default='spanish_infinitives.apkg',
        help='Output APKG file')
    args = parser.parse_args()
    main(args)

