# -*- coding: utf-8 -*-
"""clowder_test module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
from pathlib import Path

if 'CLOWDER_PROJECT_PATH' in os.environ:
    ROOT_DIR = Path(os.environ['CLOWDER_PROJECT_PATH'])
else:
    path = Path.cwd()
    while str(path) != path.root:
        clowder_test_dir = path / 'clowder_test'
        if clowder_test_dir.is_dir():
            ROOT_DIR = path
            break
        path = path.parent
