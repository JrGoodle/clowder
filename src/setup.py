"""
Setup file for clowder
"""

from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

setup(
    name='clowder-repo',
    description='A tool for managing code',
    version='3.0.0',
    url='http://clowder.cat',
    author='Joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['clowder',
              'clowder.cli',
              'clowder.error',
              'clowder.git',
              'clowder.model',
              'clowder.util',
              'clowder.yaml',
              'clowder.yaml.validation'],
    entry_points={
        'console_scripts': [
            'clowder=clowder.clowder_app:main',
        ]
    },
    install_requires=['argcomplete', 'cement', 'colorama', 'GitPython', 'PyYAML', 'termcolor', 'psutil', 'tqdm']
)
