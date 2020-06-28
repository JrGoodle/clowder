#!/usr/bin/env python

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional


repo_dir = Path(__file__).resolve().parent.parent.resolve()


def main():
    readme_path = repo_dir / 'README.md'
    readme_contents = readme_path.read_text()
    readme_contents = readme_contents.splitlines()
    readme_contents = readme_contents[2:]

    output = "\n".join(readme_contents)
    output = output.replace('](CONTRIBUTING', '](https://github.com/JrGoodle/clowder/blob/master/CONTRIBUTING')

    pattern = r'\]\(docs\/(.+?)\)'
    # matches = re.findall(pattern, output)
    replace = r'](https://github.com/JrGoodle/clowder/blob/master/docs/\1)'
    output = re.sub(pattern, replace, output)

    output = output.replace('.gif)', '.gif?raw=true)')

    processed_readme_path = repo_dir / 'README-processed.md'
    if processed_readme_path.exists():
        os.remove(str(processed_readme_path))

    with open(str(processed_readme_path), "w") as output_file:
        output_file.write(f"{output}\n")


main()
