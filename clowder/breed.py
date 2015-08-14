import os, shutil
import sh

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
    peruYAML = '.clowder/repo/peru.yaml'
    if os.path.isfile(clowderYAML):
        os.symlink(clowderYAML, 'clowder.yaml')
    if os.path.isfile(peruYAML):
        os.symlink(peruYAML, 'peru.yaml')

# def configurePeru(rootDirectory):
#     print('Updating peru.yaml')
#     clowderDirectory = os.path.join(rootDirectory, '.clowder/clowder')
#     os.chdir(rootDirectory)
#     newPeruFile = os.path.join(clowderDirectory, 'peru.yaml')
#     if os.path.isfile(newPeruFile):
#         peruFile = os.path.join(rootDirectory, 'peru.yaml')
#         shutil.copy2(newPeruFile, peruFile)
