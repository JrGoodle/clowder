"""Misc git utils"""

from typing import Dict, List, Optional, Tuple

from pygoodle.format import Format

from .constants import FETCH_URL, PUSH_URL

# TODO: Update to use ConfigParser


class ProcessOutput:

    @classmethod
    def tag_shas(cls, output: str) -> Dict[str, str]:
        # TODO: Add expected output example

        return ProcessOutput.shas(output, 'refs/tags/')

    @classmethod
    def branch_shas(cls, output: str) -> Dict[str, str]:
        # Expected output format:
        # 6def4cee3c6abe73ab2889d155421a90722282ef	refs/heads/gh-pages
        # bc787b2888acf4b7bd8351b9a72982c71c143362	refs/heads/master
        # 1ca96862f7814d9ec8b28fff17e913e11add342f	refs/heads/presentation
        # d3db093e48bd685b7eaf8da9cedcef3c9ef48b29	refs/heads/wip/force-sync

        return ProcessOutput.shas(output, 'refs/heads/')

    @classmethod
    def shas(cls, output: str, prefix: str) -> Dict[str, str]:
        # TODO: Add expected output example

        lines = output.strip().splitlines()
        items = {}
        for line in lines:
            components = line.split()
            sha = components[0].strip()
            name = Format.remove_prefix(components[1], prefix)
            items[name] = sha
        return items

    @classmethod
    def local_branches(cls, output: str) -> List[str]:
        # TODO: Add expected output example

        lines = output.splitlines()
        return [line.split()[1].strip() if line.startswith('*') else line.strip() for line in lines]

    @classmethod
    def tracking_branches(cls, output: str) -> Tuple[str, Optional[str]]:
        # Expected output format:
        # > git rev-parse --symbolic-full-name git-old@{upstream}
        # refs/heads/git
        # > git rev-parse --symbolic-full-name git-old@{upstream}
        # refs/remotes/origin/git

        if output.startswith('refs/heads'):
            remote = None
            branch = Format.remove_prefix('refs/heads', output)
        elif output.startswith('refs/remotes'):
            components = Format.remove_prefix('refs/remotes', output).split('/')
            remote = components[0]
            branch = components[1]
        else:
            raise Exception('Failed to parse tracking branch output')
        return branch, remote

    @classmethod
    def remote_branches(cls, output: str, remote: str) -> Tuple[List[str], Optional[str]]:
        # TODO: Add expected output example

        lines = output.strip().splitlines()
        branches = []
        default_branch = None
        for line in lines:
            components = line.split()
            if components[0] == 'warning:':
                continue
            if len(components) == 1:
                name = Format.remove_prefix(components[0].strip(), f'{remote}/')
                branches.append(name)
            elif len(components) == 3 and components[1] == '->':
                name = Format.remove_prefix(components[2].strip(), f'{remote}/')
                default_branch = name
            else:
                raise Exception('Wrong number of components for remote branch')
        return branches, default_branch

    @classmethod
    def remotes(cls, output: str) -> Dict[str, Dict[str, str]]:
        # Expected output format:
        # origin	git@github.com:JrGoodle/pygoodle.git (fetch)
        # origin	git@github.com:JrGoodle/pygoodle.git (push)

        lines = output.splitlines()
        line = [line.split() for line in lines]
        remotes = {}
        for components in line:
            name = components[0].strip()
            url = components[1].strip()
            kind = components[2].strip()
            if name not in remotes.keys():
                remotes[name] = {}
            if kind == '(fetch)':
                remotes[name][FETCH_URL] = url
            elif kind == '(push)':
                remotes[name][PUSH_URL] = url
            else:
                raise Exception('Unknown')
        return remotes

    @classmethod
    def submodules(cls, output: List[str]) -> Dict[str, Dict[str, str]]:
        # Expected output format for .gitmodules:
        # submodule.path/to/Optional.path path/to/Optional
        # submodule.path/to/Optional.url https://github.com/akrzemi1/Optional.git
        # submodule.path/to/Optional.branch master
        #
        # Expected output format for .git/config:
        # submodule.path/to/Optional.active true
        # submodule.path/to/Optional.url https://github.com/akrzemi1/Optional.git

        submodules = {}
        for submodule_info in output:
            info_components = submodule_info.split()
            name = info_components[0]
            value = info_components[1]
            name_components = name.split('.')
            if len(name_components) != 3 or name_components[0] != 'submodule':
                continue
            submodule_path = name_components[1]
            key = name_components[2]
            if submodule_path not in submodules.keys():
                submodules[submodule_path] = {}
            submodules[submodule_path][key] = value
        return submodules

    @classmethod
    def diff_index(cls, output: str) -> Dict[str, List[Dict[str, str]]]:
        # Expected output format
        # :000000 100644 0000000000000000000000000000000000000000 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 A	something/something.txt
        # :100644 100644 375928ea14a5a1a7e14f14a36cb0a31c417d1ca1 0000000000000000000000000000000000000000 M	README.md
        # :100644 000000 375928ea14a5a1a7e14f14a36cb0a31c417d1ca1 0000000000000000000000000000000000000000 D	README.md

        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }

        if output is None:
            return changes

        def diff_type(value: str) -> str:
            if value == 'A':
                return 'added'
            elif value == 'M':
                return 'modified'
            elif value == 'D':
                return 'deleted'
            else:
                raise Exception('Unknown diff type')

        lines = output.strip().splitlines()
        for line in lines:
            old_permissions = Format.remove_prefix(line[0].strip(), ':')
            new_permissions = line[1].strip()
            old_sha = line[2].strip()
            new_sha = line[3].strip()
            change_type = line[4].strip()
            file_path = line[5].strip()
            change = {
                'old_permissions': old_permissions,
                'new_permissions': new_permissions,
                'old_sha': old_sha,
                'new_sha': new_sha,
                'path': file_path
            }
            changes[diff_type(change_type)].append(change)
        return changes
