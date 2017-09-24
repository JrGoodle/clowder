"""Clowder yaml loading"""

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for catching too general exception Exception
# pylint: disable=W0703
# Disable errors shown by pylint for too many branches
# pylint: disable=R0912
# Disable errors shown by pylint for too many statements
# pylint: disable=R0915

def load_yaml_import_defaults(imported_defaults, defaults):
    """Load clowder projects from imported group"""
    if 'ref' in imported_defaults:
        defaults['ref'] = imported_defaults['ref']
    if 'remote' in imported_defaults:
        defaults['remote'] = imported_defaults['remote']
    if 'source' in imported_defaults:
        defaults['source'] = imported_defaults['source']
    if 'depth' in imported_defaults:
        defaults['depth'] = imported_defaults['depth']

def load_yaml_import_groups(imported_groups, groups):
    """Load clowder groups from import yaml"""
    group_names = [g['name'] for g in groups]
    for imported_group in imported_groups:
        if imported_group['name'] not in group_names:
            groups.append(imported_group)
            continue
        combined_groups = []
        for group in groups:
            if group['name'] == imported_group['name']:
                _load_yaml_import_projects(imported_group['projects'], group['projects'])
            combined_groups.append(group)
        groups = combined_groups

def _load_yaml_import_projects(imported_projects, projects):
    """Load clowder projects from imported group"""
    project_names = [p['name'] for p in projects]
    for imported_project in imported_projects:
        if imported_project['name'] not in project_names:
            projects.append(imported_project)
            continue
        combined_projects = []
        for project in projects:
            if project['name'] != imported_project['name']:
                combined_projects.append(project)
                continue
            project['path'] = imported_project['path']
            if 'depth' in imported_project:
                project['depth'] = imported_project['depth']
            if 'ref' in imported_project:
                project['ref'] = imported_project['ref']
            if 'remote' in imported_project:
                project['remote'] = imported_project['remote_name']
            if 'source' in imported_project:
                project['source'] = imported_project['source']['name']
            combined_projects.append(imported_project)
        projects = combined_projects

def load_yaml_import_sources(imported_sources, sources):
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
