"""clowder subcommands"""
import os
from clowder.model.clowder_repo import ClowderRepo
from clowder.model.clowder_yaml import ClowderYAML

def breed(root_directory, url):
    """clowder breed subcommand"""
    clowder_repo = ClowderRepo(root_directory)
    clowder_repo.clone(url)
    yaml_file = os.path.join(root_directory, 'clowder/clowder.yaml')
    symlink_clowder_yaml(root_directory, yaml_file)

def fix(root_directory, version):
    """clowder fix subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.fix_version(version)

def forall(root_directory, command):
    """clowder forall subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.forall(command)

def groom(root_directory):
    """clowder groom subcommand"""
    clowder_repo = ClowderRepo(root_directory)
    clowder_repo.groom()

def herd(root_directory, version, groups):
    """clowder herd subcommand"""
    if version == None:
        yaml_file = os.path.join(root_directory, 'clowder/clowder.yaml')
    else:
        yaml_version = 'clowder/versions/' + version + '/clowder.yaml'
        yaml_file = os.path.join(root_directory, yaml_version)
    symlink_clowder_yaml(root_directory, yaml_file)

    clowder = ClowderYAML(root_directory)
    if version == None:
        if groups == None:
            clowder.herd_all()
        else:
            clowder.herd_groups(groups)
    else:
        clowder.herd_version_all(version)

def litter(root_directory):
    """clowder litter subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.litter()

def meow(root_directory):
    """clowder meow subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.meow()

def stash(root_directory):
    """clowder stash subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.stash()

def symlink_clowder_yaml(root_directory, clowder_yaml):
    """Create clowder.yaml symlink in directory pointing to file"""
    os.chdir(root_directory)
    if os.path.isfile(clowder_yaml):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowder_yaml, 'clowder.yaml')
    else:
        print(clowder_yaml + " doesn't seem to exist")
