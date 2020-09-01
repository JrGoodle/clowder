"""Shared resources for tests"""

__defaults_yaml__ = {'ref': 'refs/heads/master', 'remote': 'origin',
                     'source': 'github', 'depth': 0, 'protocol': 'ssh'}

__github_source_yaml__ = {'name': 'github', 'url': 'github.com'}

__june_project_yaml__ = {'name': 'JrGoodle/june', 'path': 'black-cats/june'}
__kishka_project_yaml__ = {'name': 'JrGoodle/kishka', 'path': 'black-cats/kishka'}
__kit_project_yaml__ = {'name': 'JrGoodle/kit', 'path': 'black-cats/kit',
                        'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709'}

__june_group_yaml__ = {'name': 'cats', 'projects': [__june_project_yaml__]}
__kishka_group_yaml__ = {'name': 'cats', 'projects': [__kishka_project_yaml__]}
__kit_group_yaml__ = {'name': 'cats', 'projects': [__kit_project_yaml__]}

# GROUP_YAML = {'name': 'cats',
#               'projects': [{'name': 'JrGoodle/kit',
#                             'path': 'black-cats/kit',
#                             'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709',
#                             'remote': 'origin',
#                             'source': 'github'}]}
