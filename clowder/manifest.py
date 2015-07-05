import sys
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

import clowder.log
import clowder.utilities

class Manifest(object):

    def __init__(self, rootDirectory):
        manifestXML = os.path.join(rootDirectory, '.clowder/clowder/default.xml')
        self.tree = ET.parse(manifestXML)

    def getGroups(self):
        root = self.tree.getroot()
        groups = ['all']
        for element in root.findall(".//*[@groups]"):
            groups.extend([group.strip() for group in element.get("groups").split(',')])
        return set(groups)
