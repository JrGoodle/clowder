"""
Setup file for clowder
"""

from pathlib import Path
from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

repo_dir = Path(__file__).resolve().parent.parent.resolve()
process_readme_script = repo_dir / 'script' / 'process_readme.py'
exec(process_readme_script.read_text())
processed_readme = repo_dir / 'README-processed.md'
long_description = processed_readme.read_text()

setup(
    name='clowder-repo',
    description='Utility for managing multiple git repositories',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='4.0b4',
    url='http://clowder.cat',
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
              'clowder.git',
              'clowder.model',
              'clowder.util'],
    package_data={
        "clowder.util": ["clowder.schema.json", "clowder.config.schema.json"],
    },
    entry_points={
        'console_scripts': [
            'clowder=clowder.clowder_app:main',
        ]
    },
    install_requires=['argcomplete', 'colorama', 'jsonschema', 'GitPython', 'PyYAML', 'termcolor', 'psutil', 'tqdm']
)
