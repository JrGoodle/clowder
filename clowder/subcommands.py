"""clowder subcommands"""
import os
from termcolor import colored
from clowder.model.clowder_yaml import ClowderYAML
from clowder.utility.git_utilities import (
    clone_git_url_at_path,
    git_sync,
    git_fix,
    git_fix_version
)

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
    if version == None:
        # Update repo containing clowder.yaml
        git_fix(clowder_dir)
    else:
        clowder = ClowderYAML(root_directory)
        clowder.fix_version(version)
        git_fix_version(clowder_dir, version)

def groom(root_directory):
    """clowder groom subcommand"""
    # Update repo containing clowder.yaml
    clowder_dir = os.path.join(root_directory, 'clowder')
    clowder_output = colored(clowder_dir, 'green')
    print(clowder_output)
    git_sync(clowder_dir, 'refs/heads/master')
    print('')

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

def litter(root_directory):
    """clowder litter subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.litter()

def meow(root_directory):
    """clowder meow subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.status()

def symlink_clowder_yaml(root_directory, clowder_yaml):
    """Create clowder.yaml symlink in directory pointing to file"""
    os.chdir(root_directory)
    if os.path.isfile(clowder_yaml):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowder_yaml, 'clowder.yaml')
    else:
        print(clowder_yaml + " doesn't seem to exist")
