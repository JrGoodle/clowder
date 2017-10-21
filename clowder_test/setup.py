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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=['clowder_test'],
    entry_points={
        'console_scripts': [
            'clowder-test=clowder_test.cmd:main',
        ]
    },
    install_requires=['argcomplete', 'psutil']
)
