"""Test ClowderRepo class"""

import os
import sys
import unittest

from clowder.clowder_repo import ClowderRepo


class ClowderRepoTest(unittest.TestCase):
    """clowder_repo test subclass"""

    current_file_path = os.path.dirname(os.path.realpath(__file__))
    cats_example_path = os.path.abspath(os.path.join(current_file_path, '..', '..', 'examples', 'cats'))

    def setUp(self):

        self.clowder_repo = ClowderRepo()
        self.clowder_yaml_path = os.path.join(self.cats_example_path, 'clowder.yaml')

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""

        clowder_path = os.path.join(self.cats_example_path, '.clowder')
        self.assertEqual(self.clowder_repo.clowder_path, clowder_path)

    def test_link(self):
        """Test link() method"""

        self.clowder_repo.link()
        self.assertEqual(os.readlink(self.clowder_yaml_path),
                         os.path.join(self.cats_example_path, '.clowder', 'clowder.yaml'))

    def test_link_version(self):
        """Test link() method"""

        self.clowder_repo.link('v0.1')
        version_path = os.path.join('.clowder', 'versions', 'v0.1.yaml')
        self.assertEqual(os.readlink(self.clowder_yaml_path), os.path.join(self.cats_example_path, version_path))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ClowderRepoTest.cats_example_path = sys.argv.pop()
    unittest.main()
