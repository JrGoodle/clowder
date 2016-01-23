"""Test fork class"""
import unittest
from clowder.fork import Fork
from clowder.source import Source
from test.shared import GITHUB_SSH_SOURCE_YAML

class ForkTest(unittest.TestCase):
    """fork test subclass"""
    def setUp(self):
        self.name = 'test_fork'
        self.remote = 'origin'
        self.fork_yaml = {'name': self.name, 'remote': self.remote}
        self.source = Source(GITHUB_SSH_SOURCE_YAML)
        self.path = '/fork/path'
        self.fork = Fork(self.fork_yaml, self.path, self.source)

    def test_get_yaml(self):
        """Test get_yaml() method"""
        self.assertEqual(self.fork.get_yaml(), self.fork_yaml)

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.fork.path, self.path)
        self.assertEqual(self.fork.name, self.name)
        self.assertEqual(self.fork.remote, self.remote)
        self.assertEqual(self.fork.url, self.source.get_url_prefix() + self.name + ".git")

if __name__ == '__main__':
    unittest.main()
