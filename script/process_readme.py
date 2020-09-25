#!/usr/bin/env python

import os
import re
from pathlib import Path

if 'SETUP_PY' in globals():
    repo_dir = Path(globals()['REPO_DIR'])
else:
    repo_dir = Path(__file__).resolve().parent.parent.resolve()


def main():
    readme_path = repo_dir / 'README.md'
    readme_contents = readme_path.read_text()
    readme_contents = readme_contents.splitlines()
    readme_contents = readme_contents[2:]

    output = "\n".join(readme_contents)
    output = output.replace('](CONTRIBUTING', '](https://github.com/JrGoodle/clowder/blob/master/CONTRIBUTING')

    pattern = r'\]\(docs\/(.+?)\)'
    replace = r'](https://github.com/JrGoodle/clowder/blob/master/docs/\1)'
    output = re.sub(pattern, replace, output)

    if 'SETUP_PY' in globals():
        pattern = r'(## Table of Contents.+?##)'
        replace = r'##'
        output = re.sub(pattern, replace, output, flags=re.DOTALL)

    output = output.replace('.gif)', '.gif?raw=true)')

    processed_readme_path = repo_dir / 'README-processed.md'
    if processed_readme_path.exists():
        os.remove(str(processed_readme_path))

    with processed_readme_path.open('w') as output_file:
        output_file.write(f"{output}\n")


main()
