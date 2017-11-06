"""Shared resources for tests"""

__defaults_yaml__ = {'ref': 'refs/heads/master', 'remote': 'origin',
                     'source': 'github', 'depth': 0, 'protocol': 'ssh'}

__github_source_yaml__ = {'name': 'github', 'url': 'github.com'}

__jules_project_yaml__ = {'name': 'jrgoodle/jules', 'path': 'black-cats/jules'}
__kishka_project_yaml__ = {'name': 'jrgoodle/kishka', 'path': 'black-cats/kishka'}
__kit_project_yaml__ = {'name': 'jrgoodle/kit', 'path': 'black-cats/kit',
                        'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709'}

__jules_group_yaml__ = {'name': 'cats', 'projects': [__jules_project_yaml__]}
__kishka_group_yaml__ = {'name': 'cats', 'projects': [__kishka_project_yaml__]}
__kit_group_yaml__ = {'name': 'cats', 'projects': [__kit_project_yaml__]}

# GROUP_YAML = {'name': 'cats',
#               'projects': [{'name': 'jrgoodle/kit',
#                             'path': 'black-cats/kit',
#                             'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709',
#                             'remote': 'origin',
#                             'source': 'github'}]}
