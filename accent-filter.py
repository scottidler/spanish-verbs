#!/bin/env python3

import sys
import os

def filter_accent(item):
    accents = 'áéíóúÁÉÍÓÚ'
    return any(vowel in accents for vowel in item)

def main(args):
    if len(sys.argv) > 1 or not os.isatty(sys.stdin.fileno()):
        items = args if len(sys.argv) > 1 else sys.stdin
        for item in items:
            item = item.strip()
            if filter_accent(item):
                print(item)
    else:
        print("No input provided or piped. Please provide input as arguments or pipe it in.", file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])

