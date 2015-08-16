import os
import sh, yaml

class ClowderYAML(object):
    def __init__(self, rootDirectory):
        self.defaults = None
        self.groups = []
        self.remotes = []

        yamlFile = os.path.join(rootDirectory, 'clowder.yaml')
        if os.path.exists(yamlFile):
            with open(yamlFile) as file:
                parsedYAML = yaml.safe_load(file)

                self.defaults = Defaults(parsedYAML['defaults'])

                for remote in parsedYAML['remotes']:
                    self.remotes.append(Remote(remote))

                for group in parsedYAML['groups']:
                    self.groups.append(Group(rootDirectory, group, self.defaults, self.remotes))

    def getAllGroupNames(self):
        names = []
        for group in self.groups:
            names.append(group['name'])
        return names

    def sync(self):
        for group in self.groups:
            for project in group.projects:
                project.sync()

    def status(self):
        for group in self.groups:
            for project in group.projects:
                project.status()


class Defaults(object):
    def __init__(self, defaults):
        self.ref = defaults['ref']
        self.remote = defaults['remote']
        self.groups = defaults['groups']

class Remote(object):
    def __init__(self, remote):
        self.name = remote['name']
        self.url = remote['url']

class Group(object):
    def __init__(self, rootDirectory, group, defaults, remotes):
        self.name = group['name']
        self.projects = []

        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, remotes))

class Project(object):
    def __init__(self, rootDirectory, project, defaults, remotes):
        self.name = project['name']
        self.path = project['path']
        self.fullPath = os.path.join(rootDirectory, self.path)

        if 'ref' in project:
            self.ref = project['ref']
        else:
            self.ref = defaults.ref

        if 'remote' in project:
            remoteName = project['remote']
        else:
            remoteName = defaults.remote

        for remote in remotes:
            if remote.name == remoteName:
                self.remote = remote

    def sync(self):
        self._create()
        git = sh.git.bake(_cwd=self.fullPath)
        print('Syncing ' + self.name)
        git.pull(_out=process_output)

    def status(self):
        git = sh.git.bake(_cwd=self.fullPath)
        print(self.path)
        print(git.status())

    def getCurrentBranch(self):
        git = sh.git.bake(_cwd=self.fullPath)
        return str(git('rev-parse', '--abbrev-ref', 'HEAD')).rstrip('\n')

    def _create(self):
        if not os.path.isdir(os.path.join(self.fullPath, '.git')):
            if not os.path.isdir(self.fullPath):
                os.makedirs(self.fullPath)
            print('Cloning ' + self.name + ' at ' + self.path)
            git = sh.git.bake(_cwd=self.fullPath)
            git.init()
            git.remote('add', 'origin', self._getRemoteURL())
            git.fetch(_out=process_output)
            git.checkout('-t', 'origin/master')

    def _getRemoteURL(self):
        if self.remote.url.startswith('https://'):
            remoteURL = self.remote.url + "/" + self.name + ".git"
        elif self.remote.url.startswith('ssh://'):
            remoteURL = self.remote.url[6:] + ":" + self.name + ".git"
        else:
            remoteURL = None
        return remoteURL

def process_output(line):
    print(line)
