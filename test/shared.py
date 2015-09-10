"""Shared resources for tests"""
import os

CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH, '..', 'examples', 'cats'))

DEFAULTS_YAML = {'ref': 'refs/heads/master',
                 'remote': 'origin',
                 'source': 'github'}

GITHUB_SSH_SOURCE_YAML = {'name': 'github-ssh', 'url': 'ssh://git@github.com'}
GITHUB_HTTPS_SOURCE_YAML = {'name': 'github', 'url': 'https://github.com'}

JULES_PROJECT_YAML = {'name': 'jrgoodle/jules',
                      'path': 'black-cats/jules'}
KISHKA_PROJECT_YAML = {'name': 'jrgoodle/kishka',
                       'path': 'black-cats/kishka'}
KIT_PROJECT_YAML = {'name': 'jrgoodle/kit',
                    'path': 'black-cats/kit',
                    'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd'}

JULES_GROUP_YAML = {'name': 'cats',
                    'projects': [JULES_PROJECT_YAML]}
KISHKA_GROUP_YAML = {'name': 'cats',
                     'projects': [KISHKA_PROJECT_YAML]}
KIT_GROUP_YAML = {'name': 'cats',
                  'projects': [KIT_PROJECT_YAML]}

# GROUP_YAML = {'name': 'cats',
#               'projects': [{'name': 'jrgoodle/kit',
#                             'path': 'black-cats/kit',
#                             'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd',
#                             'remote': 'origin',
#                             'source': 'github'}]}
