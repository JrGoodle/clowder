"""Clowder config management"""
# import os
import yaml

class Config(object):
    """Config class for managing clowder configuration settings"""
    def __init__(self, root_directory, clowder_yaml):
        parsed_yaml = yaml.safe_load(clowder_yaml)

        # self.defaults = Defaults(parsedYAML['defaults'])
        #
        # self.remotes = []
        # for remote in parsedYAML['remotes']:
        #     self.remotes.append(Remote(remote))
        #
        # self.groups = []
        # for group in parsedYAML['groups']:
        #     self.groups.append(Group(group, self.defaults, self.remotes))
