import os, shutil
import sh

from clowder.clowderYAML import ClowderYAML

def breed(rootDirectory, url):
    dotClowderDirectory = os.path.join(rootDirectory, '.clowder')
    os.mkdir(dotClowderDirectory)

    git = sh.git.bake(_cwd=dotClowderDirectory)
    git.clone(url, 'repo')

    clowderDirectory = os.path.join(dotClowderDirectory, 'repo')
    git = sh.git.bake(_cwd=clowderDirectory)
    git.fetch('--all', '--prune', '--tags')

    # Create symlinks
    os.chdir(rootDirectory)
    clowderYAML = '.clowder/repo/clowder.yaml'
    if os.path.isfile(clowderYAML):
        os.symlink(clowderYAML, 'clowder.yaml')

def fix(rootDirectory, version):
    repoDir = os.path.join(rootDirectory, '.clowder/repo')
    git = sh.git.bake(_cwd=repoDir)

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
    repoDir = os.path.join(rootDirectory, '.clowder/repo')
    git = sh.git.bake(_cwd=repoDir)
    git.fetch('--all', '--prune', '--tags')
    git.pull()

def herd(rootDirectory, version):
    clowder = ClowderYAML(rootDirectory)
    clowder.sync()

def meow(rootDirectory):
    clowder = ClowderYAML(rootDirectory)
    clowder.status()
