import os
import sh, yaml

class Config(object):
    def __init__(self, rootDirectory, clowderYAML):
        parsedYAML = yaml.safe_load(clowderYAML)

        self.defaults = Defaults(parsedYAML['defaults'])

        self.remotes = []
        for remote in parsedYAML['remotes']:
            self.remotes.append(Remote(remote))

        self.groups = []
        for group in parsedYAML['groups']:
            self.groups.append(Group(group, self.defaults, self.remotes))

    # def getCurrentProjectNames(self):
    #     configFile = os.path.join(self.rootDirectory, '.clowder/config.yaml')
    #     if os.path.exists(configFile):
    #         with open(configFile) as file:
    #             yamlConfig = yaml.safe_load(file)
    #             return yamlConfig["currentProjectNames"]
    #     return None

    # def getSnapshotNames(self):
    #     snapshotsDir = os.path.join(self.rootDirectory, '.clowder/snapshots')
    #     if os.path.exists(snapshotsDir):
    #         files = os.listdir(snapshotsDir)
    #         snapshots = []
    #         for name in files:
    #             snapshots.append(clowder.utilities.rchop(name, '.yaml'))
    #         return snapshots
    #     return None
