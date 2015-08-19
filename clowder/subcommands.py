"""clowder subcommands"""
import os
import sh
# Disable errors shown by pylint for sh.git
# pylint: disable=E1101

from clowder.clowder_yaml import ClowderYAML
from clowder.utilities import clone_git_url_at_path, symlink_clowder_yaml

def breed(root_directory, url):
    """clowder breed subcommand"""
    clowder_dir = os.path.join(root_directory, 'clowder')
    clone_git_url_at_path(url, clowder_dir)
    # Create clowder.yaml symlink
    yaml_file = os.path.join(clowder_dir, 'clowder.yaml')
    symlink_clowder_yaml(root_directory, yaml_file)

def fix(root_directory, version):
    """clowder fix subcommand"""
    clowder_dir = os.path.join(root_directory, 'clowder')
    git = sh.git.bake(_cwd=clowder_dir)

    if version == None:
        # Update repo containing clowder.yaml
        git.add('clowder.yaml')
        git.commit('-m', 'Update clowder.yaml')
    else:
        clowder = ClowderYAML(root_directory)
        clowder.fix_version(version)
        git.add('versions')
        git.commit('-m', 'Fix version ' + version + '.yaml')

    git.pull()
    git.push()

def groom(root_directory):
    """clowder groom subcommand"""
    # Update repo containing clowder.yaml
    clowder_dir = os.path.join(root_directory, 'clowder')
    git = sh.git.bake(_cwd=clowder_dir)
    git.fetch('--all', '--prune', '--tags')
    git.pull()

def herd(root_directory, version, sync_all):
    """clowder herd subcommand"""
    if version == None:
        yaml_file = os.path.join(root_directory, 'clowder/clowder.yaml')
        symlink_clowder_yaml(root_directory, yaml_file)
        clowder = ClowderYAML(root_directory)
        if sync_all:
            clowder.sync_all()
        else:
            clowder.sync()
    else:
        yaml_version = 'clowder/versions/' + version + '/clowder.yaml'
        yaml_file = os.path.join(root_directory, yaml_version)
        symlink_clowder_yaml(root_directory, yaml_file)
        clowder = ClowderYAML(root_directory)
        if sync_all:
            clowder.sync_version_all(version)
        else:
            clowder.sync_version(version)

def meow(root_directory):
    """clowder meow subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.status()
