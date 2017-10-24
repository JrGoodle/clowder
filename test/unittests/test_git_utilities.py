"""Test group class"""

import os
import sys
import unittest

from clowder.git.repo import GitRepo


class GitUtilitiesTest(unittest.TestCase):
    """git_utilities test subclass"""

    current_file_path = os.path.dirname(os.path.realpath(__file__))
    cats_example_path = os.path.abspath(os.path.join(current_file_path, '..', '..', 'examples', 'cats'))

    def setUp(self):

        self.jules_project_path = os.path.join(self.cats_example_path, 'black-cats', 'jules')
        self.kishka_project_path = os.path.join(self.cats_example_path, 'black-cats', 'kishka')
        self.kit_project_path = os.path.join(self.cats_example_path, 'black-cats', 'kit')
        self.sasha_project_path = os.path.join(self.cats_example_path, 'black-cats', 'sasha')
        self.remote = 'origin'
        self.branch_ref = 'refs/heads/master'
        self.tag_ref = 'refs/tags/v1.0'
        self.sha_ref = '6ce5538d2c09fda2f56a9ca3859f5e8cfe706bf0'

    def test_git_current_branch(self):
        """Test git_current_branch() function"""

        repo = GitRepo(self.kit_project_path, self.remote, self.branch_ref)
        self.assertEqual(repo.current_branch(), 'master')

    def test_git_sha_long(self):
        """Test git_sha_long() function"""

        repo = GitRepo(self.sasha_project_path, self.remote, self.branch_ref)
        self.assertEqual(repo.sha(), self.sha_ref)

    def test_git_is_detached(self):
        """Test git_is_detached() function"""

        repo = GitRepo(self.jules_project_path, self.remote, self.branch_ref)
        self.assertFalse(repo.is_detached())
        repo = GitRepo(self.kit_project_path, self.remote, self.branch_ref)
        self.assertFalse(repo.is_detached())
        repo = GitRepo(self.sasha_project_path, self.remote, self.branch_ref)
        self.assertTrue(repo.is_detached())

    def test_git_is_dirty(self):
        """Test git_is_dirty() function"""

        repo = GitRepo(self.jules_project_path, self.remote, self.branch_ref)
        self.assertFalse(repo.is_dirty())
        repo = GitRepo(self.kishka_project_path, self.remote, self.branch_ref)
        self.assertTrue(repo.is_dirty())
        repo = GitRepo(self.kit_project_path, self.remote, self.branch_ref)
        self.assertFalse(repo.is_dirty())

    def test_ref_type_branch(self):
        """Test ref_type() function for branch ref"""

        self.assertEqual(GitRepo.ref_type(self.branch_ref), 'branch')

    def test_ref_type_sha(self):
        """Test ref_type() function for sha ref"""

        self.assertEqual(GitRepo.ref_type(self.sha_ref), 'sha')

    def test_ref_type_tag(self):
        """Test ref_type() function for tag ref"""

        self.assertEqual(GitRepo.ref_type(self.tag_ref), 'tag')

    def test_ref_type_unknown(self):
        """Test ref_type() function for unknown ref type"""

        self.assertEqual(GitRepo.ref_type('42'), 'unknown')

    def test_truncate_ref_branch(self):
        """Test _truncate_ref() function for branch ref"""

        self.assertEqual(GitRepo.truncate_ref(self.branch_ref), 'master')

    def test_truncate_ref_sha(self):
        """Test _truncate_ref() function for sha ref"""

        self.assertEqual(GitRepo.truncate_ref(self.sha_ref), self.sha_ref)

    def test_truncate_ref_tag(self):
        """Test _truncate_ref() function for tag ref"""

        self.assertEqual(GitRepo.truncate_ref(self.tag_ref), 'v1.0')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        GitUtilitiesTest.cats_example_path = sys.argv.pop()
    unittest.main()
