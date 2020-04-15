"""
Setup file for clowder test runner
"""

from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

setup(
    name='clowder-test',
    description='Test runner for clowder command',
    version='0.1.0',
    url='http://clowder.cat',
    author='Joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    packages=['clowder_test',
              'clowder_test.cli'],
    entry_points={
        'console_scripts': [
            'clowder-test=clowder_test.clowder_test_app:main',
        ]
    },
    install_requires=['argcomplete', 'cement', 'colorama', 'coverage', 'cprint', 'psutil', 'termcolor']
)
