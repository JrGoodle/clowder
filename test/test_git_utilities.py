"""Test group class"""
import unittest
from clowder.utility.git_utilities import (
    git_ref_type,
    git_truncate_ref
)

class GroupTest(unittest.TestCase):
    """group test subclass"""
    def setUp(self):
        self.branch_ref = 'refs/heads/master'
        self.tag_ref = 'refs/tags/v1.0'
        self.sha_ref = '7083e8840e1bb972b7664cfa20bbd7a25f004018'
        self.unknown_ref = 'unknown'

    def test_git_ref_type_branch(self):
        """Test git_ref_type() function for branch ref"""
        self.assertEqual(git_ref_type(self.branch_ref), 'branch')

    def test_git_ref_type_sha(self):
        """Test git_ref_type() function for sha ref"""
        self.assertEqual(git_ref_type(self.sha_ref), 'sha')

    def test_git_ref_type_tag(self):
        """Test git_ref_type() function for tag ref"""
        self.assertEqual(git_ref_type(self.tag_ref), 'tag')

    def test_git_ref_type_unknown(self):
        """Test git_ref_type() function for unknown ref type"""
        self.assertEqual(git_ref_type(self.unknown_ref), 'unknown')

    def test_git_truncate_ref_branch(self):
        """Test git_truncate_ref() function for branch ref"""
        self.assertEqual(git_truncate_ref(self.branch_ref), 'master')

    def test_git_truncate_ref_sha(self):
        """Test git_truncate_ref() function for sha ref"""
        self.assertEqual(git_truncate_ref(self.sha_ref), self.sha_ref)

    def test_git_truncate_ref_tag(self):
        """Test git_truncate_ref() function for tag ref"""
        self.assertEqual(git_truncate_ref(self.tag_ref), 'v1.0')

if __name__ == '__main__':
    unittest.main()
