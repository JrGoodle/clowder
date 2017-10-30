"""
Setup file for clowder
"""

from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

setup(
    name='clowder-repo',
    description='A tool for managing code',
    version='2.4.0',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=['clowder',
              'clowder.error',
              'clowder.git',
              'clowder.model',
              'clowder.util',
              'clowder.yaml',
              'clowder.yaml.validation'],
    entry_points={
        'console_scripts': [
            'clowder=clowder.cmd:main',
        ]
    },
    install_requires=['argcomplete', 'colorama', 'GitPython', 'PyYAML', 'termcolor', 'psutil', 'tqdm']
)
