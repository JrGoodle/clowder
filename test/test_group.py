"""Test group class"""
import os, unittest
from clowder.group import Group
from clowder.source import Source

CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH, '..', 'examples', 'cats'))

class GroupTest(unittest.TestCase):
    """group test subclass"""
    def setUp(self):
        defaults_yaml = {'ref': 'refs/heads/master',
                         'remote': 'origin',
                         'source': 'github'}
        sources = [Source({'name': 'github-ssh', 'url': 'ssh://git@github.com'}),
                   Source({'name': 'github', 'url': 'https://github.com'})]
        jules_project_yaml = {'name': 'jrgoodle/jules',
                              'path': 'black-cats/jules'}
        kishka_project_yaml = {'name': 'jrgoodle/kishka',
                               'path': 'black-cats/kishka'}
        kit_project_yaml = {'name': 'jrgoodle/kit',
                            'path': 'black-cats/kit',
                            'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd'}
        jules_group_yaml = {'name': 'cats',
                            'projects': [jules_project_yaml]}
        kishka_group_yaml = {'name': 'cats',
                             'projects': [kishka_project_yaml]}
        kit_group_yaml = {'name': 'cats',
                          'projects': [kit_project_yaml]}
        self.jules_group = Group(CATS_EXAMPLE_PATH, jules_group_yaml, defaults_yaml, sources)
        self.kishka_group = Group(CATS_EXAMPLE_PATH, kishka_group_yaml, defaults_yaml, sources)
        self.kit_group = Group(CATS_EXAMPLE_PATH, kit_group_yaml, defaults_yaml, sources)

    def test_get_yaml(self):
        """Test get_yaml() method"""
        group_yaml = {'name': 'cats',
                      'projects': [{'name': 'jrgoodle/kit',
                                    'path': 'black-cats/kit',
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
