"""Test group class"""
import os
import unittest
from clowder.utility.git_utilities import (
    git_current_branch,
    git_is_detached,
    git_is_dirty,
    git_sha_long,
    _ref_type,
    _truncate_ref
)
from test.shared import CATS_EXAMPLE_PATH

class GitUtilitiesTest(unittest.TestCase):
    """git_utilities test subclass"""
    def setUp(self):
        self.jules_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'jules')
        self.kishka_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'kishka')
        self.kit_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'kit')
        self.sasha_project_path = os.path.join(CATS_EXAMPLE_PATH, 'black-cats', 'sasha')
        self.branch_ref = 'refs/heads/master'
        self.tag_ref = 'refs/tags/v1.0'
        self.sha_ref = '6ce5538d2c09fda2f56a9ca3859f5e8cfe706bf0'

    def test_git_current_branch(self):
        """Test git_current_branch() function"""
        self.assertEqual(git_current_branch(self.kit_project_path), 'master')

    def test_git_sha_long(self):
        """Test git_sha_long() function"""
        self.assertEqual(git_sha_long(self.sasha_project_path), self.sha_ref)

    def test_git_is_detached(self):
        """Test git_is_detached() function"""
        self.assertFalse(git_is_detached(self.jules_project_path))
        self.assertFalse(git_is_detached(self.kit_project_path))
        self.assertTrue(git_is_detached(self.sasha_project_path))

    def test_git_is_dirty(self):
        """Test git_is_detached() function"""
        self.assertFalse(git_is_dirty(self.jules_project_path))
        self.assertTrue(git_is_dirty(self.kishka_project_path))
        self.assertFalse(git_is_dirty(self.kit_project_path))

    def test_ref_type_branch(self):
        """Test _ref_type() function for branch ref"""
        self.assertEqual(_ref_type(self.branch_ref), 'branch')

    def test_ref_type_sha(self):
        """Test _ref_type() function for sha ref"""
        self.assertEqual(_ref_type(self.sha_ref), 'sha')

    def test_ref_type_tag(self):
        """Test _ref_type() function for tag ref"""
        self.assertEqual(_ref_type(self.tag_ref), 'tag')

    def test_ref_type_unknown(self):
        """Test _ref_type() function for unknown ref type"""
        self.assertEqual(_ref_type('42'), 'unknown')

    def test_truncate_ref_branch(self):
        """Test _truncate_ref() function for branch ref"""
        self.assertEqual(_truncate_ref(self.branch_ref), 'master')

    def test_truncate_ref_sha(self):
        """Test _truncate_ref() function for sha ref"""
        self.assertEqual(_truncate_ref(self.sha_ref), self.sha_ref)

    def test_truncate_ref_tag(self):
        """Test _truncate_ref() function for tag ref"""
        self.assertEqual(_truncate_ref(self.tag_ref), 'v1.0')

if __name__ == '__main__':
    unittest.main()
