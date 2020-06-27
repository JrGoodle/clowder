#!/usr/bin/env python

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional


if 'GH_PAGES_DIR' not in os.environ:
    print('GH_PAGES_DIR not set')
    exit(1)

gh_pages_dir = Path(os.environ['GH_PAGES_DIR'])
print(gh_pages_dir)
path = Path.cwd()


def main():
    readme_path = path / 'README.md'
    readme_contents = readme_path.read_text()
    readme_contents = readme_contents.splitlines()
    readme_contents = readme_contents[2:]

    output = "\n".join(readme_contents)
    output = output.replace('](CONTRIBUTING', '](https://github.com/JrGoodle/clowder/blob/master/CONTRIBUTING')

    pattern = r'\]\(docs\/(.+?(?<!\.gif))\)'
    matches = re.findall(pattern, output)
    replace = r'](https://github.com/JrGoodle/clowder/blob/master/docs/\1)'
    output = re.sub(pattern, replace, output)

    with open(str( gh_pages_dir / 'index.md'), "w") as text_file:
        text_file.write(f"{output}\n")


main()
