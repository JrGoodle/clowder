"""Test project class"""
import os, unittest
from clowder.source import Source
from clowder.project import Project

CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH, '..', 'examples', 'cats'))

class ProjectTest(unittest.TestCase):
    """project test subclass"""
    def setUp(self):
        self.jules_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'jules')
        self.kishka_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'kishka')
        self.kit_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'kit')
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
        self.jules_project = Project(CATS_EXAMPLE_PATH, jules_project_yaml,
                                     defaults_yaml, sources)
        self.kishka_project = Project(CATS_EXAMPLE_PATH, kishka_project_yaml,
                                      defaults_yaml, sources)
        self.kit_project = Project(CATS_EXAMPLE_PATH, kit_project_yaml,
                                   defaults_yaml, sources)

    def test_exists(self):
        """Test exists() method"""
        self.assertFalse(self.jules_project.exists())
        self.assertTrue(self.kit_project.exists())

    def test_full_path(self):
        """Test full_path() method"""
        self.assertEqual(self.kit_project.full_path(), self.kit_project_path)

    def test_is_dirty(self):
        """Test is_dirty() method"""
        self.assertTrue(self.kishka_project.is_dirty())
        self.assertFalse(self.kit_project.is_dirty())

    def test_is_valid(self):
        """Test is_valid() method"""
        self.assertTrue(self.jules_project.is_valid())
        self.assertFalse(self.kishka_project.is_valid())
        self.assertTrue(self.kit_project.is_valid())

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.kit_project.name, 'jrgoodle/kit')
        self.assertEqual(self.kit_project.path, 'black-cats/kit')
        self.assertEqual(self.kit_project.ref, 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd')
        self.assertEqual(self.kit_project.remote_name, 'origin')
        self.assertEqual(self.kit_project.root_directory, CATS_EXAMPLE_PATH)
        self.assertEqual(self.kit_project.url, 'https://github.com/jrgoodle/kit.git')

    def test_get_yaml(self):
        """Test get_yaml() method"""
        project_yaml = {'name': 'jrgoodle/kit',
                        'path': 'black-cats/kit',
                        'ref': 'da5c3d32ec2c00aba4a9f7d822cce2c727f7f5dd',
                        'remote': 'origin',
                        'source': 'github'}
        self.assertEqual(self.kit_project.get_yaml(), project_yaml)

if __name__ == '__main__':
    unittest.main()
