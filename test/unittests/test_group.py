"""Test group class"""

import os
import sys
import unittest

from clowder.model import Defaults
from clowder.model.group import Group
from clowder.model import Source
from unittests.shared import (
    __defaults_yaml__,
    __github_source_yaml__,
    __june_group_yaml__,
    __kishka_group_yaml__,
    __kit_group_yaml__
)


class GroupTest(unittest.TestCase):
    """group test subclass"""

    current_file_path = os.path.dirname(os.path.realpath(__file__))
    cats_example_path = os.path.abspath(os.path.join(current_file_path, '..', '..', 'examples', 'cats'))

    def setUp(self):

        sources = [Source(__github_source_yaml__)]
        self.june_group = Group(__june_group_yaml__, Defaults(__defaults_yaml__), sources)
        self.kishka_group = Group(__kishka_group_yaml__, Defaults(__defaults_yaml__), sources)
        self.kit_group = Group(__kit_group_yaml__, Defaults(__defaults_yaml__), sources)

    def test_get_yaml(self):
        """Test get_yaml() method"""

        group_yaml = {'name': 'cats',
                      'projects': [{'name': 'jrgoodle/kit',
                                    'path': 'black-cats/kit',
                                    'depth': 0,
                                    'recursive': False,
                                    'ref': 'f2e20031ddce5cb097105f4d8ccbc77f4ac20709',
                                    'remote': 'origin',
                                    'source': 'github'}]}
        self.assertEqual(self.kit_group.get_yaml(), group_yaml)

    def test_is_dirty(self):
        """Test is_dirty() method"""

        self.assertTrue(self.kishka_group.is_dirty())
        self.assertFalse(self.kit_group.is_dirty())

    def test_is_valid(self):
        """Test is_valid() method"""

        self.assertTrue(self.june_group.is_valid())
        self.assertFalse(self.kishka_group.is_valid())
        self.assertTrue(self.kit_group.is_valid())

    def test_member_variables(self):
        """Test the state of all project member variables initialized"""

        self.assertEqual(self.kit_group.name, 'cats')
        # self.assertEqual(self.group.projects, [Project()])

    def test_projects_exist(self):
        """Test projects_exist() method"""

        self.assertFalse(self.june_group.existing_projects())
        self.assertTrue(self.kit_group.existing_projects())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        GroupTest.cats_example_path = sys.argv.pop()
    unittest.main()
