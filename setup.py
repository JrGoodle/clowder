"""
Setup file for clowder
"""
import sys
from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

if sys.version_info[0] < 3:
    sys.exit('This script requires python 3.0 or higher to run.')

setup(
    name='clowder-repo',
    description='A tool for managing code',
    version='2.1.0',
    url='http://clowder.cat',
    author='Joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=['clowder', 'clowder.utility'],
    entry_points={
        'console_scripts': [
            'clowder=clowder.cmd:main',
        ]
    },
    install_requires=['argcomplete', 'colorama', 'GitPython', 'PyYAML', 'termcolor']
)
