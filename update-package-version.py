#!/usr/bin/python3

# run in same directory as package.json
# accepts version tag as first argument

import json
import argparse
import sys

if len(sys.argv) != 2:
    print("Usage: update-package-version.py <new version>")
    sys.exit(1)

new_version = sys.argv[1]

def update(filename):
    # want the generated file to look as similar to the original as possible...

    contents = open(filename, 'r').read()
    guessed_tab_size = 2 if '\n  "version"' in contents else 4
    has_trailing_newline = contents.endswith('\n')

    data = json.loads(contents)

    version = data['version'].split('.')
    version[2] = new_version
    data['version'] = '.'.join(version)

    new_contents = json.dumps(
        data,
        separators=(',', ': '),
        indent=guessed_tab_size,
        ensure_ascii=False # deprecation warnings in package-lock.json can contain emoji
    )

    with open(filename, 'w') as f:
        f.write(new_contents)
        if has_trailing_newline:
            f.write('\n')

    print(f"Updated {filename}")

update('package.json')
update('package-lock.json')
