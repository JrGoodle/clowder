import os, shutil
import sh

def truncateGitRef(ref):
    gitBranch = "refs/heads/"
    gitTag = "refs/tags/"
    if ref.startswith(gitBranch):
        length = len(gitBranch)
    elif ref.startswith(gitTag):
        length = len(gitTag)
    else:
        length = 0
    return ref[length:]

def cloneGitUrlAtPath(url, repoPath):
    if not os.path.isdir(os.path.join(repoPath, '.git')):
        if not os.path.isdir(repoPath):
            os.makedirs(repoPath)
        print('Cloning git repo at ' + repoPath)
        git = sh.git.bake(_cwd=repoPath)
        git.init()
        git.remote('add', 'origin', url)
        git.fetch('--all', '--prune', '--tags', _out=process_output)
        git.checkout('-t', 'origin/master')

def process_output(line):
    print(line)

def symlinkClowderYAML(rootDirectory, clowderYAML):
    os.chdir(rootDirectory)
    if os.path.isfile(clowderYAML):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowderYAML, 'clowder.yaml')
    else:
        print(clowderYAML + " doesn't seem to exist")
