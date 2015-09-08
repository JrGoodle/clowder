"""Test project class"""
import os, unittest
from clowder.source import Source
from clowder.project import Project

CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH, '..', 'examples', 'cats'))

class ProjectTest(unittest.TestCase):
    """project test subclass"""
    def setUp(self):
        self.project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'kit')
        defaults = {'ref': 'refs/heads/master',
                    'remote': 'origin',
                    'source': 'github'}
        sources = [Source({'name': 'github-ssh', 'url': 'ssh://git@github.com'}),
                   Source({'name': 'github', 'url': 'https://github.com'})]
        project = {'name': 'jrgoodle/kit',
                   'path': 'black-cats/kit',
                   'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd'}
        self.project = Project(CATS_EXAMPLE_PATH, project, defaults, sources)

    def test_exists(self):
        """Test exists() method"""
        self.assertTrue(self.project.exists())

    def test_full_path(self):
        """Test full_path() method"""
        self.assertEqual(self.project.full_path(), self.project_path)

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.project.name, 'jrgoodle/kit')
        self.assertEqual(self.project.path, 'black-cats/kit')
        self.assertEqual(self.project.ref, 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd')
        self.assertEqual(self.project.remote_name, 'origin')
        self.assertEqual(self.project.root_directory, CATS_EXAMPLE_PATH)
        self.assertEqual(self.project.url, 'https://github.com/jrgoodle/kit.git')

    def test_get_yaml(self):
        """Test get_yaml() method"""
        project_dict = {'name': 'jrgoodle/kit',
                        'path': 'black-cats/kit',
                        'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd',
                        'remote': 'origin',
                        'source': 'github'}
        self.assertEqual(self.project.get_yaml(), project_dict)

if __name__ == '__main__':
    unittest.main()
