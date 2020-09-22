"""
Setup file for clowder
"""

import os
import sys
from pathlib import Path
from setuptools import setup

from build_manpages import build_manpages, get_build_py_cmd, get_install_cmd
from setuptools.command.build_py import build_py
from setuptools.command.install import install

from clowder import __version__

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

if 'READTHEDOCS' in os.environ:
    long_description = 'Utility for managing multiple git repositories'
else:
    repo_dir = Path(__file__).resolve().parent.resolve()
    process_readme_script = repo_dir / 'script' / 'process_readme.py'
    exec(process_readme_script.read_text(), {'SETUP_PY': True, 'REPO_DIR': str(repo_dir)})
    processed_readme = repo_dir / 'README-processed.md'
    long_description = processed_readme.read_text()

setup(
    name='clowder-repo',
    description='Utility for managing multiple git repositories',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    url='https://github.com/JrGoodle/clowder',
    project_urls={
        "Documentation": "https://clowder.readthedocs.io/en/latest/"
    },
    author='Joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Version Control :: Git'
    ],
    packages=['clowder',
              'clowder.cli',
              'clowder.config',
              'clowder.git_project',
              'clowder.data',
              'clowder.data.model',
              'clowder.util'],
    package_data={
        "clowder.util": ["clowder.schema.json", "clowder.config.schema.json"],
    },
    entry_points={
        'console_scripts': [
            'clowder=clowder.clowder_app:main',
        ]
    },
    install_requires=['argcomplete', 'colorama', 'jsonschema', 'GitPython',
                      'PyYAML', 'termcolor', 'psutil', 'tqdm'],
    tests_require=['pytest', 'pytest-bdd', 'pytest-xdist'],
    cmdclass={
        'build_manpages': build_manpages,
        'build_py': get_build_py_cmd(build_py),
        'install': get_install_cmd(install),
    }
)
