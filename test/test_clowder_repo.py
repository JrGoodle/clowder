"""Test ClowderRepo class"""
import os
import sys
import unittest
from clowder.clowder_repo import ClowderRepo

class ClowderRepoTest(unittest.TestCase):
    """clowder_repo test subclass"""

    CURRENT_FILE_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    CATS_EXAMPLE_PATH = os.path.abspath(os.path.join(CURRENT_FILE_DIR_PATH,
                                                     '..', 'examples', 'cats'))

    def setUp(self):
        self.clowder_repo = ClowderRepo(self.CATS_EXAMPLE_PATH)
        self.clowder_yaml_path = os.path.join(self.CATS_EXAMPLE_PATH, 'clowder.yaml')

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.clowder_repo.root_directory, self.CATS_EXAMPLE_PATH)
        clowder_path = os.path.join(self.CATS_EXAMPLE_PATH, '.clowder')
        self.assertEqual(self.clowder_repo.clowder_path, clowder_path)

    def test_link(self):
        """Test link() method"""
        self.clowder_repo.link()
        self.assertEqual(os.readlink(self.clowder_yaml_path),
                         os.path.join(self.CATS_EXAMPLE_PATH, '.clowder', 'clowder.yaml'))

    def test_link_version(self):
        """Test link() method"""
        self.clowder_repo.link('v0.1')
        version_path = os.path.join('.clowder', 'versions', 'v0.1', 'clowder.yaml')
        self.assertEqual(os.readlink(self.clowder_yaml_path),
                         os.path.join(self.CATS_EXAMPLE_PATH, version_path))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ClowderRepoTest.CATS_EXAMPLE_PATH = sys.argv.pop()
    unittest.main()
