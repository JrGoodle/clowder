"""
Setup file for clowder
"""

from setuptools import setup

# Written according to the docs at
# https://packaging.python.org/en/latest/distributing.html

setup(
    name='clowder-repo',
    description='A tool for managing code',
    version='4.0b1',
    url='http://clowder.cat',
    author='Joe DeCapo',
    author_email='joe@polka.cat',
    license='MIT',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
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
