"""clowder subcommands"""
import os
from clowder.model.clowder_repo import ClowderRepo
from clowder.model.clowder_yaml import ClowderYAML

def breed(root_directory, url):
    """clowder breed subcommand"""
    clowder_repo = ClowderRepo(root_directory)
    clowder_repo.clone(url)
    # Create clowder.yaml symlink
    yaml_file = os.path.join(root_directory, 'clowder/clowder.yaml')
    symlink_clowder_yaml(root_directory, yaml_file)

def fix(root_directory, version):
    """clowder fix subcommand"""
    if version == None:
        pass
    else:
        clowder = ClowderYAML(root_directory)
        clowder.validate_all()
        clowder.fix_version(version)

def forall(root_directory, command):
    """clowder forall subcommand"""
    clowder = ClowderYAML(root_directory)
    clowder.forall(command)

def groom(root_directory):
    """clowder groom subcommand"""
    # Update repo containing clowder.yaml
    clowder_repo = ClowderRepo(root_directory)
    clowder_repo.herd()

def herd(root_directory, version):
    """clowder herd subcommand"""
    if version == None:
        yaml_file = os.path.join(root_directory, 'clowder/clowder.yaml')
        symlink_clowder_yaml(root_directory, yaml_file)
        clowder = ClowderYAML(root_directory)
        clowder.herd_all()
    else:
        yaml_version = 'clowder/versions/' + version + '/clowder.yaml'
        yaml_file = os.path.join(root_directory, yaml_version)
        symlink_clowder_yaml(root_directory, yaml_file)
        clowder = ClowderYAML(root_directory)
        clowder.herd_version_all(version)

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
