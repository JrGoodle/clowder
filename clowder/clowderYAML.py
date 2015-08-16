import os
import sh, yaml

class ClowderYAML(object):
    def __init__(self, rootDirectory):
        self.rootDirectory = rootDirectory

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
                    self.groups.append(Group(self.rootDirectory, group, self.defaults, self.remotes))

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

    def fixVersion(self, version):
        versionsDirectory = os.path.join(self.rootDirectory, '.clowder/repo/versions')
        if not os.path.exists(versionsDirectory):
            os.mkdir(versionsDirectory)

        yamlFile = os.path.join(versionsDirectory, version + '.yaml')
        if not os.path.exists(yamlFile):
            with open(yamlFile, 'w') as file:
                yaml.dump(self.getYAML(), file, default_flow_style=False)

    def getYAML(self):
        groupsYAML = []
        for group in self.groups:
            groupsYAML.append(group.getYAML())

        remotesYAML = []
        for remote in self.remotes:
            remotesYAML.append(remote.getYAML())

        return {'defaults': self.defaults.getYAML(),
                'remotes': remotesYAML,
                'groups': groupsYAML}

class Defaults(object):
    def __init__(self, defaults):
        self.ref = defaults['ref']
        self.remote = defaults['remote']
        self.groups = defaults['groups']

    def getYAML(self):
        return {'ref': self.ref, 'remote': self.remote, 'groups':self.groups}

class Remote(object):
    def __init__(self, remote):
        self.name = remote['name']
        self.url = remote['url']

    def getYAML(self):
        return {'name': self.name, 'url': self.url}

class Group(object):
    def __init__(self, rootDirectory, group, defaults, remotes):
        self.name = group['name']
        self.projects = []

        for project in group['projects']:
            self.projects.append(Project(rootDirectory, project, defaults, remotes))

    def getYAML(self):
        projectsYAML = []

        for project in self.projects:
            projectsYAML.append(project.getYAML())
        return {'name': self.name, 'projects': projectsYAML}

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
            self.remoteName = project['remote']
        else:
            self.remoteName = defaults.remote

        for remote in remotes:
            if remote.name == self.remoteName:
                self.remote = remote

    def getYAML(self):
        return {'name': self.name,
                'path': self.path,
                'ref': self.getCurrentSHA(),
                'remote': self.remoteName}

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

    def getCurrentSHA(self):
        git = sh.git.bake(_cwd=self.fullPath)
        return str(git('rev-parse', 'HEAD')).rstrip('\n')

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
