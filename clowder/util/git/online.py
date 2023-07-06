"""Misc git utils"""

from pathlib import Path
from subprocess import CompletedProcess
from typing import Dict, List, Optional

import pygoodle.command as cmd
import pygoodle.filesystem as fs
from pygoodle.format import Format

from .constants import HEAD, ORIGIN
from .process_output import ProcessOutput


class GitOnline:

    @classmethod
    def pull(cls, path: Path, remote: Optional[str] = None, branch: Optional[str] = None,
             rebase: bool = False, prune: bool = False, tags: bool = False,
             jobs: Optional[int] = None, no_edit: bool = False, autostash: bool = False,
             depth: Optional[int] = None, fetch_all: bool = False) -> CompletedProcess:
        """Pull upstream changes"""

        refspec = None
        if branch is not None:
            remote = ORIGIN if remote is None else remote
            refspec = f'refs/heads/{branch}:refs/remotes/{remote}/heads/{branch}'

        remote = '' if remote is None else remote
        refspec = '' if refspec is None else refspec

        args = ''
        if rebase:
            args += ' --rebase '
        if prune:
            args += ' --prune '
        if tags:
            args += ' --tags '
        if no_edit:
            args += ' --no-edit '
        if autostash:
            args += ' --autostash '
        if jobs is not None:
            args += f' --jobs={jobs} '
        if depth is not None:
            args += f' --depth={depth} '
        if fetch_all:
            args += f' --all '
        return cmd.run(f'git pull {args} {remote} {refspec}', cwd=path)

    @classmethod
    def pull_lfs(cls, path: Path) -> CompletedProcess:
        """Pull lfs files"""

        return cmd.run('git lfs pull', cwd=path)

    # See: https://github.blog/2020-12-21-get-up-to-speed-with-partial-clone-and-shallow-clone/
    @classmethod
    def clone(cls, path: Path, url: str, depth: Optional[int] = None, branch: Optional[str] = None,
              tag: Optional[str] = None, jobs: Optional[int] = None, single_branch: bool = False,
              blobless: bool = False, treeless: bool = False, origin: Optional[str] = None) -> CompletedProcess:
        if path.is_dir():
            if fs.has_contents(path):
                raise Exception(f'Existing directory at clone path {path}')
            fs.remove_dir(path)

        args = ''
        if branch is not None:
            args += f' --branch {branch} '
        elif tag is not None:
            args += f' --branch {tag} '

        if single_branch:
            args += ' --single-branch '
        if jobs is not None:
            args += f' --jobs {jobs} '
        if depth is not None:
            args += f' --depth {depth} '
        if origin is not None:
            args += f' --origin {origin} '

        assert not (blobless and treeless)
        if blobless:
            args += ' --filter=blob:none '
        elif treeless:
            args += ' --filter=tree:0 '

        return cmd.run(f'git clone {args} {url} {path}')

    @classmethod
    def push(cls, path: Path, remote: Optional[str] = None, local_branch: Optional[str] = None,
             remote_branch: Optional[str] = None, force: bool = False, set_upstream: bool = False) -> CompletedProcess:
        refspec = None
        if remote_branch is not None:
            remote = ORIGIN if remote is None else remote
            local_branch = HEAD if local_branch is None else local_branch
            refspec = f'refs/heads/{local_branch}:refs/heads/{remote_branch}'
        elif local_branch is not None:
            remote = ORIGIN if remote is None else remote
            remote_branch = local_branch
            refspec = f'refs/heads/{local_branch}:refs/heads/{remote_branch}'

        remote = '' if remote is None else remote
        refspec = '' if refspec is None else refspec

        args = ''
        if force:
            args += ' --force '
        if set_upstream:
            args += ' --set-upstream '

        return cmd.run(f'git push {args} {remote} {refspec}', cwd=path)

    @classmethod
    def fetch(cls, path: Path, prune: bool = False, prune_tags: bool = False, tags: bool = False,
              depth: Optional[int] = None, remote: Optional[str] = None, branch: Optional[str] = None,
              unshallow: bool = False, jobs: Optional[int] = None, fetch_all: bool = False,
              print_output: bool = True) -> CompletedProcess:

        refspec = None
        if branch is not None:
            remote = ORIGIN if remote is None else remote
            refspec = f'refs/heads/{branch}:refs/remotes/{remote}/heads/{branch}'

        remote = '' if remote is None else remote
        refspec = '' if refspec is None else refspec

        args = ''
        if prune:
            args += ' --prune '
        if prune_tags:
            args += ' --prune-tags '
        if tags:
            args += ' --tags '
        if depth is not None:
            args += f' --depth {depth}'
        if unshallow:
            args += ' --unshallow '
        if jobs is not None:
            args += ' --jobs '
        if fetch_all:
            args += ' --all '

        return cmd.run(f"git fetch {args} {remote} {refspec}", cwd=path, print_output=print_output)

    @classmethod
    def delete_remote_tag(cls, path: Path, tag: str, remote: Optional[str] = None,
                          force: bool = False) -> CompletedProcess:
        refspec = f':refs/tags/{tag}'
        remote = ORIGIN if remote is None else remote
        args = ''
        if force:
            args += ' --force '
        return cmd.run(f'git push {remote} {args} {refspec}', cwd=path)

    @classmethod
    def delete_remote_branch(cls, path: Path, branch: str, remote: str = ORIGIN,
                             force: bool = False) -> CompletedProcess:
        refspec = f':refs/heads/{branch}'
        remote = ORIGIN if remote is None else remote
        args = ''
        if force:
            args += ' --force '
        return cmd.run(f'git push {remote} {args} {refspec}', cwd=path)

    @classmethod
    def branch_exists_at_remote_url(cls, url: str, branch: str) -> bool:
        output = cmd.get_stdout(f'git ls-remote --heads {url} {branch}')
        if output is None:
            # TODO: Should this return None?
            return False
        return bool(output)

    @classmethod
    def branch_exists_on_remote(cls, path: Path, branch: str, remote: str = ORIGIN) -> bool:
        output = cmd.get_stdout(f'git ls-remote --heads {remote} {branch}', cwd=path)
        if output is None:
            # TODO: Should this return None?
            return False
        return bool(output)

    @classmethod
    def get_default_branch(cls, url: str) -> Optional[str]:
        """Get default branch from remote repo"""

        command = f'git ls-remote --symref {url} {HEAD}'
        output = cmd.get_stdout(command)
        if output is None:
            return None
        output_list = output.split()
        branch = [Format.remove_prefix(chunk, 'refs/heads/')
                  for chunk in output_list if chunk.startswith('refs/heads/')]
        return branch[0]

    @classmethod
    def submodule_update(cls, path: Path, init: bool = False, depth: Optional[int] = None, single_branch: bool = False,
                         jobs: Optional[int] = None, recursive: bool = False, remote: bool = False,
                         no_fetch: bool = False, checkout: bool = False, rebase: bool = False, merge: bool = False,
                         paths: Optional[List[Path]] = None) -> CompletedProcess:
        args = ''
        if init:
            args += ' --init '
        if single_branch:
            args += ' --single-branch '
        if jobs is not None:
            args += f' --jobs {jobs} '
        if depth is not None:
            args += f' --depth {depth} '
        if recursive is not None:
            args += ' --recursive '
        if remote:
            args += ' --remote '
        if no_fetch:
            args += ' --no-fetch '

        # TODO: Validate that at most one of these is True
        if checkout:
            args += ' --checkout '
        if merge:
            args += ' --merge '
        if rebase:
            args += ' --rebase '

        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ''
        return cmd.run(f'git submodule update {args} {paths}', cwd=path)

    @classmethod
    def get_remote_tag_sha(cls, path: Path, name: str, remote: str = ORIGIN) -> Optional[str]:
        tags = GitOnline.get_remote_tags_info(path, remote=remote)
        sha = [sha for t, sha in tags.items() if t == name]
        return sha[0] if sha else None

    @classmethod
    def get_remote_tags_info(cls, path: Path = Path.cwd(), remote: str = ORIGIN) -> Dict[str, str]:
        output = cmd.get_stdout(f"git ls-remote --tags {remote}", cwd=path)
        if output is None:
            return {}
        return ProcessOutput.tag_shas(output)

    @classmethod
    def get_remote_tag(cls, path: Path, name: str, remote: str = ORIGIN) -> Optional[str]:
        tags = GitOnline.get_remote_tags_info(path, remote=remote)
        tag = [t for t, sha in tags.items() if t == name]
        return tag[0] if tag else None

    @classmethod
    def get_remote_branches_info(cls, path: Path = Path.cwd(), remote: str = ORIGIN) -> Dict[str, str]:
        output = cmd.get_stdout(f'git ls-remote --heads {remote}', cwd=path)
        if output is None:
            return {}
        return ProcessOutput.branch_shas(output)
