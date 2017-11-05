"""Test source class"""

import sys
import unittest

from clowder.model.source import Source
from unittests.shared import __github_source_yaml__


class SourceTest(unittest.TestCase):
    """source test subclass"""

    def setUp(self):

        self.source = Source(__github_source_yaml__)

    def test_get_yaml(self):
        """Test get_yaml() method"""

        self.assertEqual(self.source.get_yaml(), __github_source_yaml__)

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""

        self.assertEqual(self.source.name, 'github')
        self.assertEqual(self.source.url, 'github.com')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _ = sys.argv.pop()
    unittest.main()
