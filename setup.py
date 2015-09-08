"""
Setup file for clowder
"""
from setuptools import setup
import sys

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

if sys.version_info[0] < 3:
    sys.exit('This script requires python 3.0 or higher to run.')

setup(
    name='clowder',
    description='A tool for managing code',
    version='0.7.0',
    url='http://clowder.cat',
    author='joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['clowder', 'clowder.utility'],
    entry_points={
        'console_scripts': [
            'clowder=clowder.cmd:main',
        ]
    },
    install_requires=['argcomplete', 'colorama', 'emoji', 'GitPython', 'PyYAML', 'termcolor']
)
