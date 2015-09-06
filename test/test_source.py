"""Test source class"""
import unittest
from clowder.source import Source

class SourceTest(unittest.TestCase):
    """source test subclass"""
    def setUp(self):
        self.ssh_source_dict = {'name': 'github-ssh', 'url': 'ssh://git@github.com'}
        self.https_source_dict = {'name': 'github-https', 'url': 'https://github.com'}
        self.ssh_source = Source(self.ssh_source_dict)
        self.https_source = Source(self.https_source_dict)

    def test_ssh_url_prefix(self):
        """Test ssh url prefix"""
        self.assertEqual(self.ssh_source.get_url_prefix(), 'git@github.com:')

    def test_https_url_prefix(self):
        """Test https url prefix"""
        self.assertEqual(self.https_source.get_url_prefix(), 'https://github.com/')

    def test_get_yaml(self):
        """Test get_yaml() method"""
        self.assertEqual(self.ssh_source.get_yaml(), self.ssh_source_dict)
        self.assertEqual(self.https_source.get_yaml(), self.https_source_dict)

if __name__ == '__main__':
    unittest.main()
