"""Clowder utilities"""
import os

def symlink_clowder_yaml(root_directory, clowder_yaml):
    """Create clowder.yaml symlink in directory pointing to file"""
    os.chdir(root_directory)
    if os.path.isfile(clowder_yaml):
        if os.path.isfile('clowder.yaml'):
            os.remove('clowder.yaml')
        os.symlink(clowder_yaml, 'clowder.yaml')
    else:
        print(clowder_yaml + " doesn't seem to exist")

def get_yaml_path(root_directory, version):
    if version == None:
        return os.path.join(root_directory, 'clowder/clowder.yaml')
    else:
        yaml_version = 'clowder/versions/' + version + '/clowder.yaml'
        return os.path.join(root_directory, yaml_version)
