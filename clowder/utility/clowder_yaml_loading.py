"""Clowder yaml loading"""
import sys
from termcolor import colored
from clowder.utility.print_utilities import (
    # format_invalid_entries_error,
    print_error,
    print_invalid_yaml_error
)

def load_yaml_base(parsed_yaml, combined_yaml):
    """Load clowder from base yaml file"""
    combined_yaml['defaults'] = parsed_yaml['defaults']
    if 'depth' not in parsed_yaml['defaults']:
        combined_yaml['defaults']['depth'] = 0
    combined_yaml['sources'] = parsed_yaml['sources']
    combined_yaml['groups'] = parsed_yaml['groups']

def load_yaml_import(parsed_yaml, combined_yaml):
    """Load clowder from import yaml file"""
    if 'defaults' in parsed_yaml:
        _load_yaml_import_defaults(parsed_yaml['defaults'],
                                   combined_yaml['defaults'])
    if 'sources' in parsed_yaml:
        _load_yaml_import_sources(parsed_yaml['sources'],
                                  combined_yaml['sources'])
    if 'groups' in parsed_yaml:
        _load_yaml_import_groups(parsed_yaml['groups'],
                                 combined_yaml['groups'])

def _load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group"""
    if 'recursive' in imported_defaults:
        defaults['recursive'] = imported_defaults['recursive']
    if 'ref' in imported_defaults:
        defaults['ref'] = imported_defaults['ref']
    if 'remote' in imported_defaults:
        defaults['remote'] = imported_defaults['remote']
    if 'source' in imported_defaults:
        defaults['source'] = imported_defaults['source']
    if 'depth' in imported_defaults:
        defaults['depth'] = imported_defaults['depth']

def _load_yaml_import_groups(imported_groups, groups):
    """Load clowder groups from import yaml"""
    group_names = [g['name'] for g in groups]
    for imported_group in imported_groups:
        if imported_group['name'] not in group_names:
            groups.append(imported_group)
            continue
        combined_groups = []
        for group in groups:
            if group['name'] == imported_group['name']:
                if 'recursive' in imported_groups:
                    group['recursive'] = imported_groups['recursive']
                if 'ref' in imported_group:
                    group['ref'] = imported_group['ref']
                if 'remote' in imported_group:
                    group['remote'] = imported_group['remote']
                if 'source' in imported_group:
                    group['source'] = imported_group['source']
                if 'depth' in imported_group:
                    group['depth'] = imported_group['depth']
                if 'projects' in imported_group:
                    _load_yaml_import_projects(imported_group['projects'], group['projects'])
            combined_groups.append(group)
        groups = combined_groups

def _load_yaml_import_projects(imported_projects, projects):
    """Load clowder projects from imported group"""
    project_names = [p['name'] for p in projects]
    for imported_project in imported_projects:
        if imported_project['name'] not in project_names:
            if 'path' not in imported_project:
                # error = format_invalid_entries_error('defaults', defaults, yaml_file)
                error = colored(' - Missing path in new project', 'red')
                print_invalid_yaml_error()
                print_error(error)
                sys.exit(1)
            projects.append(imported_project)
            continue
        combined_projects = []
        for project in projects:
            if project['name'] != imported_project['name']:
                combined_projects.append(project)
                continue
            if 'path' in imported_project:
                project['path'] = imported_project['path']
            if 'depth' in imported_project:
                project['depth'] = imported_project['depth']
            if 'recursive' in imported_project:
                project['recursive'] = imported_project['recursive']
            if 'ref' in imported_project:
                project['ref'] = imported_project['ref']
            if 'remote' in imported_project:
                project['remote'] = imported_project['remote']
            if 'fork' in imported_project:
                project['fork'] = imported_project['fork']
            if 'source' in imported_project:
                project['source'] = imported_project['source']['name']
            combined_projects.append(imported_project)
        projects = combined_projects

def _load_yaml_import_sources(imported_sources, sources):
    """Load clowder sources from import yaml"""
    source_names = [s['name'] for s in sources]
    for imported_source in imported_sources:
        if imported_source['name'] not in source_names:
            sources.append(imported_source)
            continue
        combined_sources = []
        for source in sources:
            if source.name == imported_source['name']:
                combined_sources.append(imported_source)
            else:
                combined_sources.append(source)
        sources = combined_sources
