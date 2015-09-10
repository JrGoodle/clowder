"""Test source class"""
import unittest
from clowder.source import Source
from test.shared import (
    GITHUB_HTTPS_SOURCE_YAML,
    GITHUB_SSH_SOURCE_YAML
)

class SourceTest(unittest.TestCase):
    """source test subclass"""
    def setUp(self):
        self.ssh_source = Source(GITHUB_SSH_SOURCE_YAML)
        self.https_source = Source(GITHUB_HTTPS_SOURCE_YAML)

    def test_get_yaml(self):
        """Test get_yaml() method"""
        self.assertEqual(self.ssh_source.get_yaml(), GITHUB_SSH_SOURCE_YAML)
        self.assertEqual(self.https_source.get_yaml(), GITHUB_HTTPS_SOURCE_YAML)

    def test_https_url_prefix(self):
        """Test https url prefix"""
        self.assertEqual(self.https_source.get_url_prefix(), 'https://github.com/')

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""
        self.assertEqual(self.ssh_source.name, 'github-ssh')
        self.assertEqual(self.ssh_source.url, 'ssh://git@github.com')
        self.assertEqual(self.https_source.name, 'github')
        self.assertEqual(self.https_source.url, 'https://github.com')

    def test_ssh_url_prefix(self):
        """Test ssh url prefix"""
        self.assertEqual(self.ssh_source.get_url_prefix(), 'git@github.com:')

if __name__ == '__main__':
    unittest.main()
