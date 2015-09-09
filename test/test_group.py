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
        project_yaml = {'name': 'jrgoodle/kit',
                        'path': 'black-cats/kit',
                        'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd'}
        group_yaml = {'name': 'cats',
                      'projects': [project_yaml]}
        self.group = Group(CATS_EXAMPLE_PATH, group_yaml, defaults_yaml, sources)

    def test_exists(self):
        """Test exists() method"""
        self.assertTrue(self.group.projects_exist())

    def test_get_yaml(self):
        """Test get_yaml() method"""
        group_yaml = {'name': 'cats',
                      'projects': [{'name': 'jrgoodle/kit',
                                    'path': 'black-cats/kit',
                                    'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd',
                                    'remote': 'origin',
                                    'source': 'github'}]}
        self.assertEqual(self.group.get_yaml(), group_yaml)

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.group.name, 'cats')
        # self.assertEqual(self.group.projects, [Project()])

if __name__ == '__main__':
    unittest.main()
