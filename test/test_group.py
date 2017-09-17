"""Test group class"""
import unittest
from clowder.group import Group
from clowder.source import Source
from test.shared import (
    CATS_EXAMPLE_PATH,
    DEFAULTS_YAML,
    GITHUB_HTTPS_SOURCE_YAML,
    GITHUB_SSH_SOURCE_YAML,
    JULES_GROUP_YAML,
    KISHKA_GROUP_YAML,
    KIT_GROUP_YAML
)

class GroupTest(unittest.TestCase):
    """group test subclass"""
    def setUp(self):
        sources = [Source(GITHUB_SSH_SOURCE_YAML),
                   Source(GITHUB_HTTPS_SOURCE_YAML)]
        self.jules_group = Group(CATS_EXAMPLE_PATH, JULES_GROUP_YAML, DEFAULTS_YAML, sources)
        self.kishka_group = Group(CATS_EXAMPLE_PATH, KISHKA_GROUP_YAML, DEFAULTS_YAML, sources)
        self.kit_group = Group(CATS_EXAMPLE_PATH, KIT_GROUP_YAML, DEFAULTS_YAML, sources)

    def test_get_yaml(self):
        """Test get_yaml() method"""
        group_yaml = {'name': 'cats',
                      'projects': [{'name': 'jrgoodle/kit',
                                    'path': 'black-cats/kit',
                                    'depth': 0,
                                    'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd',
                                    'remote': 'origin',
                                    'source': 'github'}]}
        self.assertEqual(self.kit_group.get_yaml(), group_yaml)

    def test_is_dirty(self):
        """Test is_dirty() method"""
        self.assertTrue(self.kishka_group.is_dirty())
        self.assertFalse(self.kit_group.is_dirty())

    def test_is_valid(self):
        """Test is_valid() method"""
        self.assertTrue(self.jules_group.is_valid())
        self.assertFalse(self.kishka_group.is_valid())
        self.assertTrue(self.kit_group.is_valid())

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.kit_group.name, 'cats')
        # self.assertEqual(self.group.projects, [Project()])

    def test_projects_exist(self):
        """Test projects_exist() method"""
        self.assertFalse(self.jules_group.projects_exist())
        self.assertTrue(self.kit_group.projects_exist())

if __name__ == '__main__':
    unittest.main()
