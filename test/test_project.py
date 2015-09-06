"""Test project class"""
import unittest
from clowder.source import Source
from clowder.project import Project

class ProjectTest(unittest.TestCase):
    """project test subclass"""
    def setUp(self):
        defaults = {'ref': 'refs/heads/master',
                    'remote': 'origin',
                    'source': 'github'}
        sources = [Source({'name': 'github', 'url': 'ssh://git@github.com'}),
                   Source({'name': 'github-https', 'url': 'https://github.com'})]
        project = {'name': 'test/project',
                   'path': 'test/path',
                   'ref': '7083e8840e1bb972b7664cfa20bbd7a25f004018'}
        root_directory = '/root/directory'
        self.project = Project(root_directory, project, defaults, sources)

    def test_get_yaml(self):
        """Test get_yaml() method"""
        # project_dict = {'name': 'test/project',
        #                 'path': 'test/path',
        #                 'ref': '7083e8840e1bb972b7664cfa20bbd7a25f004018',
        #                 'remote': 'origin',
        #                 'source': 'github'}
        # self.assertEqual(self.project.get_yaml(), project_dict)
        pass

if __name__ == '__main__':
    unittest.main()
