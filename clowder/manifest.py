import os
import xml.etree.ElementTree as ET

import clowder.utilities

class Manifest(object):

    def __init__(self, rootDirectory):
        self.clowderDirectory = os.path.join(rootDirectory, '.clowder/clowder')
        manifestXML = os.path.join(self.clowderDirectory, 'default.xml')
        self.tree = ET.parse(manifestXML)

    def getGroups(self):
        root = self.tree.getroot()
        groups = ['all']
        for element in root.findall(".//*[@groups]"):
            groups.extend([group.strip() for group in element.get("groups").split(',')])
        return set(groups)

    def getVersions(self):
        versions = []
        for file in os.listdir(self.clowderDirectory):
            if file.endswith('.xml'):
                name = clowder.utilities.rchop(file, '.xml')
                if name != 'default':
                    versions.append(name)
        return versions
