"""Test project class"""
import os
import sys
import unittest
from clowder.source import Source
from clowder.project import Project
from test.shared import (
    DEFAULTS_YAML,
    GITHUB_HTTPS_SOURCE_YAML,
    GITHUB_SSH_SOURCE_YAML,
    JULES_GROUP_YAML,
    JULES_PROJECT_YAML,
    KISHKA_GROUP_YAML,
    KISHKA_PROJECT_YAML,
    KIT_GROUP_YAML,
    KIT_PROJECT_YAML
)

class ProjectTest(unittest.TestCase):
    """project test subclass"""

    CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH,
                                                     '..', 'examples', 'cats'))

    def setUp(self):
        # self.jules_project_path = os.path.join(self.CATS_EXAMPLE_PATH, 'black-cats', 'jules')
        # self.kishka_project_path = os.path.join(self.CATS_EXAMPLE_PATH, 'black-cats', 'kishka')
        self.kit_project_path = os.path.join(self.CATS_EXAMPLE_PATH, 'black-cats', 'kit')
        sources = [Source(GITHUB_SSH_SOURCE_YAML),
                   Source(GITHUB_HTTPS_SOURCE_YAML)]
        self.jules_project = Project(self.CATS_EXAMPLE_PATH, JULES_PROJECT_YAML,
                                     JULES_GROUP_YAML, DEFAULTS_YAML, sources)
        self.kishka_project = Project(self.CATS_EXAMPLE_PATH, KISHKA_PROJECT_YAML,
                                      KISHKA_GROUP_YAML, DEFAULTS_YAML, sources)
        self.kit_project = Project(self.CATS_EXAMPLE_PATH, KIT_PROJECT_YAML,
                                   KIT_GROUP_YAML, DEFAULTS_YAML, sources)

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
        self.assertEqual(self.kit_project.ref, 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709')
        self.assertEqual(self.kit_project.remote_name, 'origin')
        self.assertEqual(self.kit_project.root_directory, self.CATS_EXAMPLE_PATH)
        self.assertEqual(self.kit_project.url, 'https://github.com/jrgoodle/kit.git')

    def test_get_yaml(self):
        """Test get_yaml() method"""
        project_yaml = {'name': 'jrgoodle/kit',
                        'path': 'black-cats/kit',
                        'depth': 0,
                        'recursive': False,
                        'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709',
                        'remote': 'origin',
                        'source': 'github'}
        self.assertEqual(self.kit_project.get_yaml(), project_yaml)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ProjectTest.CATS_EXAMPLE_PATH = sys.argv.pop()
    unittest.main()
