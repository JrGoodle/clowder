import os, shutil
import sh

from clowder.clowderYAML import ClowderYAML
from clowder.utilities import *

def breed(rootDirectory, url):
    clowderDir = os.path.join(rootDirectory, 'clowder')
    cloneGitUrlAtPath(url, clowderDir)
    # Create clowder.yaml symlink
    yamlFile = os.path.join(clowderDir, 'clowder.yaml')
    symlinkClowderYAML(rootDirectory, yamlFile)

def fix(rootDirectory, version):
    clowderDir = os.path.join(rootDirectory, 'clowder')
    git = sh.git.bake(_cwd=clowderDir)

    if version == None:
        # Update repo containing clowder.yaml
        git.add('clowder.yaml')
        git.commit('-m', 'Update clowder.yaml')
    else:
        clowder = ClowderYAML(rootDirectory)
        clowder.fixVersion(version)
        git.add('versions')
        git.commit('-m', 'Fix version ' + version + '.yaml')

    git.pull()
    git.push()

def groom(rootDirectory):
    # Update repo containing clowder.yaml
    clowderDir = os.path.join(rootDirectory, 'clowder')
    git = sh.git.bake(_cwd=clowderDir)
    git.fetch('--all', '--prune', '--tags')
    git.pull()

def herd(rootDirectory, version):
    if version == None:
        yamlFile = os.path.join(rootDirectory, 'clowder/clowder.yaml')
        symlinkClowderYAML(rootDirectory, yamlFile)
        clowder = ClowderYAML(rootDirectory)
        clowder.sync()
    else:
        yamlVersion = 'clowder/versions/' + version + '/clowder.yaml'
        yamlFile = os.path.join(rootDirectory, yamlVersion)
        symlinkClowderYAML(rootDirectory, yamlFile)
        clowder = ClowderYAML(rootDirectory)
        clowder.syncVersion(version)

def meow(rootDirectory):
    clowder = ClowderYAML(rootDirectory)
    clowder.status()
