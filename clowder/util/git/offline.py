"""Misc git utils"""

from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess
from typing import Dict, List, Optional, Tuple

import pygoodle.command as cmd
import pygoodle.filesystem as fs
from pygoodle.format import Format

from .constants import HEAD, FETCH_URL, PUSH_URL
from .process_output import ProcessOutput


class GitOffline:

    @classmethod
    def get_remote_fetch_url(cls, path: Path, remote: str) -> Optional[str]:
        remotes = GitOffline.get_remotes_info(path)
        if remote not in remotes.keys():
            return None
        return remotes[remote][FETCH_URL]

    @classmethod
    def get_remote_push_url(cls, path: Path, remote: str) -> Optional[str]:
        remotes = GitOffline.get_remotes_info(path)
        if remote not in remotes.keys():
            return None
        return remotes[remote][PUSH_URL]

    @classmethod
    def get_remotes_info(cls, path: Path) -> Dict[str, Dict[str, str]]:
        output = cmd.get_stdout('git remote -v', cwd=path)
        if output is None:
            return {}
        remotes = ProcessOutput.remotes(output)
        return remotes

    @classmethod
    def get_remote_url(cls, path: Path, remote_name: str) -> Optional[str]:
        """Get url of remote

        :param Path path: Path to git repo
        :param str remote_name: Remote name
        :return: URL of remote
        """

        return cmd.get_stdout(f'git remote get-url {remote_name}', cwd=path)

    @classmethod
    def create_remote(cls, path: Path, name: str, url: str, fetch: bool = False, tags: bool = False) -> None:
        args = ''
        if fetch:
            args += ' -f '
        if tags:
            args += ' --tags '
        cmd.run_silent(f'git remote add {name} {url}', cwd=path)

    @classmethod
    def find_rev_by_timestamp(cls, path: Path, timestamp: str, ref: str, author: Optional[str] = None) -> Optional[str]:
        """Find rev by timestamp

        :param Path path: Path to git repo
        :param str timestamp: Commit ref timestamp
        :param str ref: Reference ref
        :param Optional[str] author: Commit author
        :return: Commit sha at or before timestamp
        """

        args = ''
        if author is not None:
            args += f' --author {author} '
        return cmd.get_stdout(f'git log -1 --format=%H --before={timestamp} {ref}', cwd=path)

    @classmethod
    def install_lfs_hooks(cls, path: Path, local: bool = False) -> CompletedProcess:
        """Install git lfs hooks"""

        args = ''
        if local:
            args = ' --local '
        return cmd.run(f'git lfs install {args}', cwd=path)

    @classmethod
    def rename_remote(cls, path: Path, old_name: str, new_name: str) -> CompletedProcess:
        return cmd.run(f'git remote rename {old_name} {new_name}', cwd=path)

    @classmethod
    def get_default_branch(cls, path: Path, remote: str) -> Optional[str]:
        """Get default branch from local repo"""

        try:
            command = f'git symbolic-ref refs/remotes/{remote}/{HEAD}'
            output = cmd.get_stdout(command, cwd=path)
            if output is None:
                return None
            output_list = output.split()
            branch = [Format.remove_prefix(chunk, f'refs/remotes/{remote}/') for chunk in output_list
                      if chunk.startswith(f'refs/remotes/{remote}/')]
            return branch[0]
        except CalledProcessError:
            return None

    @classmethod
    def save_default_branch(cls, git_dir: Path, remote: str, branch: str) -> None:
        """Save default branch"""

        if not git_dir.exists():
            return
        remote_head_ref = git_dir / 'refs' / 'remotes' / remote / HEAD
        if not remote_head_ref.exists():
            fs.make_dir(remote_head_ref.parent, exist_ok=True)
            contents = f'ref: refs/remotes/{remote}/{branch}'
            remote_head_ref.touch()
            remote_head_ref.write_text(contents)

    @classmethod
    def current_timestamp(cls, path: Path) -> Optional[str]:
        """Current timestamp of HEAD commit"""

        return cmd.get_stdout('git log -1 --format=%cI', cwd=path)

    @classmethod
    def is_repo_cloned(cls, path: Path) -> bool:
        """Check if a git repository exists

        :param Path path: Repo path
        :return: True, if .git directory exists inside path
        """

        git_dir = GitOffline.git_dir(path)
        if git_dir is None:
            return False
        return git_dir.is_dir() and fs.has_contents(git_dir)

    @classmethod
    def is_dirty(cls, path: Path) -> bool:
        GitOffline.update_index(path, refresh=True)
        changes = GitOffline.diff_index(path)
        return changes is not None

    @classmethod
    def diff_index(cls, path: Path, treeish: str = HEAD) -> Optional[str]:
        return cmd.get_stdout(f'git diff-index {treeish}', cwd=path)

    @classmethod
    def update_index(cls, path: Path, refresh: bool = False) -> CompletedProcess:
        args = ''
        if refresh:
            args += ' --refresh '
        return cmd.run_silent(f'git update-index {args}', path)

    @classmethod
    def get_diff_index_info(cls, path: Path) -> Dict[str, List[Dict[str, str]]]:
        GitOffline.update_index(path, refresh=True)
        output = GitOffline.diff_index(path)
        return ProcessOutput.diff_index(output)

    @classmethod
    def is_rebase_in_progress(cls, path: Path) -> bool:
        rebase_merge = path / ".git" / "rebase-merge"
        rebase_apply = path / ".git" / "rebase-apply"
        rebase_merge_exists = rebase_merge.exists() and rebase_merge.is_dir()
        rebase_apply_exists = rebase_apply.exists() and rebase_apply.is_dir()
        return rebase_merge_exists or rebase_apply_exists

    @classmethod
    def get_local_branches_info(cls, path: Path) -> List[str]:
        output = cmd.get_stdout("git branch", cwd=path)
        if output is None:
            return []
        branches = ProcessOutput.local_branches(output)
        return branches

    @classmethod
    def get_local_tags_info(cls, path: Path) -> Dict[str, str]:
        output = cmd.get_stdout("git show-ref --tags", cwd=path)
        if output is None:
            return {}
        return ProcessOutput.tag_shas(output)

    @classmethod
    def get_untracked_files(cls, path: Path) -> List[Path]:
        output = cmd.get_stdout('git ls-files . --exclude-standard --others', cwd=path)
        if output is None:
            return []
        return [Path(line.strip()) for line in output.splitlines()]

    @classmethod
    def new_commits_count(cls, path: Path, upstream: bool = False) -> int:
        """Returns the number of new commits

        :param Path path: Path to git repo
        :param bool upstream: Whether to find number of new upstream or local commits
        :return: Int number of new commits
        """

        local_branch = GitOffline.current_branch(path)
        upstream_branch = GitOffline.get_upstream_branch(path, local_branch)
        if local_branch == HEAD or upstream_branch is None:
            return 0

        try:
            local_sha = GitOffline.get_branch_sha(path, local_branch)
            remote_sha = GitOffline.get_branch_sha(path, upstream_branch[0], remote=upstream_branch[1])
            commits = f'{local_sha}...{remote_sha}'
            output = cmd.get_stdout(f'git rev-list --count --left-right {commits}', cwd=path)
            if output is None:
                return 0
            index = 1 if upstream else 0
            return int(output.split()[index])
        except (CalledProcessError, ValueError):
            return 0

    @classmethod
    def has_untracked_files(cls, path: Path) -> bool:
        files = GitOffline.get_untracked_files(path)
        return bool(files)

    @classmethod
    def is_submodule_placeholder(cls, path: Path) -> bool:
        return path.is_dir() and fs.is_empty_dir(path)

    @classmethod
    def is_repo_submodule(cls, path: Path) -> bool:
        parent_repo = GitOffline.find_parent_repo(path)
        return parent_repo is not None

    @classmethod
    def find_parent_repo(cls, path: Path) -> Optional[Path]:
        path = path.parent
        while str(path) != path.root:
            git_dir = path / '.git'
            if git_dir.exists():
                return path
            path = path.parent

    @classmethod
    def get_submodule_commit(cls, path: Path, submodule_path: Path) -> Optional[str]:
        output = cmd.get_stdout(f'git ls-tree {HEAD} {submodule_path}', cwd=path)
        if output is None:
            return None
        components = output.split()
        return components[2]

    @classmethod
    def get_submodules_info(cls, path: Path) -> Dict[str, Dict[str, str]]:
        submodules = GitOffline.get_submodules_info_from_gitmodules(path)
        git_config_submodules = GitOffline.get_submodules_info_from_git_config(path)
        for name, values in git_config_submodules.items():
            if name not in submodules:
                continue
            for key, value in values.items():
                submodules[name][key] = value
        return submodules

    @classmethod
    def get_submodules_info_from_gitmodules(cls, path: Path) -> Dict[str, Dict[str, str]]:
        output = GitOffline.get_config_info(path, 'submodule', path / '.gitmodules')
        submodules = ProcessOutput.submodules(output)
        return submodules

    @classmethod
    def get_submodules_info_from_git_config(cls, path: Path) -> Dict[str, Dict[str, str]]:
        git_dir = GitOffline.git_dir(path)
        if git_dir is None:
            return {}
        output = GitOffline.get_config_info(path, 'submodule', git_dir / 'config')
        submodules = ProcessOutput.submodules(output)
        return submodules

    @classmethod
    def get_config_info(cls, path: Path, name: str, file: Path) -> List[str]:
        output = cmd.get_stdout(f'git config --file {file} --get-regexp {name}', cwd=path)
        if output is None:
            return []
        return output.splitlines()

    @classmethod
    def git_dir(cls, path: Path) -> Optional[Path]:
        repo_git_path = path / '.git'
        if not repo_git_path.exists():
            return None
        if repo_git_path.is_dir():
            return repo_git_path
        contents = repo_git_path.read_text().strip()
        gitdir_prefix = 'gitdir: '
        if not contents.startswith(gitdir_prefix):
            return None
        git_dir_path = Format.remove_prefix(contents, gitdir_prefix)
        git_dir = repo_git_path.parent / git_dir_path
        return git_dir.resolve(strict=False)

    @classmethod
    def is_submodule_initialized(cls, path: Path, submodule_path: Path) -> bool:
        submodules = GitOffline.get_submodules_info_from_git_config(path)
        return str(submodule_path) in submodules.keys()

    @classmethod
    def is_submodule_cloned(cls, path: Path, submodule_path: Path) -> bool:
        git_dir = GitOffline.git_dir(path)
        if git_dir is None:
            return False
        full_path = path / submodule_path
        return git_dir.is_dir() and fs.has_contents(git_dir) and full_path.is_dir() and fs.has_contents(full_path)

    @classmethod
    def lfs_hooks_installed(cls, path: Path) -> bool:
        hooks = [
            ['git lfs pre-push', '.git/hooks/pre-push'],
            ['git lfs post-checkout', '.git/hooks/post-checkout'],
            ['git lfs post-commit', '.git/hooks/post-commit'],
            ['git lfs post-merge', '.git/hooks/post-merge']
        ]

        for hook in hooks:
            command = hook[0]
            file_path = path / hook[1]
            if not file_path.exists():
                return False
            file_text = file_path.read_text()
            if command not in file_text:
                return False
        return True

    @classmethod
    def lfs_filters_installed(cls, path: Path) -> bool:
        lfs_filters = [
            'smudge',
            'clean',
            'process',
            'required'
        ]

        for lfs_filter in lfs_filters:
            result = cmd.run_silent(f'git config --get filter.lfs.{lfs_filter}', cwd=path)
            if result.returncode != 0:
                return False
        return True

    @classmethod
    def uninstall_lfs_hooks(cls, path: Path) -> List[CompletedProcess]:
        commands = [
            'git lfs uninstall --local',
            'git lfs uninstall --system',
            'git lfs uninstall'
        ]

        results = []
        for command in commands:
            result = cmd.run_silent(command)
            results.append(result)

        assert not GitOffline.lfs_hooks_installed(path)
        return results

    @classmethod
    def uninstall_lfs_filters(cls, path: Path) -> List[CompletedProcess]:
        commands = [
            'git config --system --unset filter.lfs.clean',
            'git config --system --unset filter.lfs.smudge',
            'git config --system --unset filter.lfs.process',
            'git config --system --unset filter.lfs.required'
        ]

        results = []
        for command in commands:
            result = cmd.run_silent(command)
            results.append(result)

        assert not GitOffline.lfs_filters_installed(path)
        return results

    @classmethod
    def is_lfs_file_pointer(cls, path: Path, file: str) -> bool:
        output = cmd.get_stdout(f'git lfs ls-files -I "{file}"', cwd=path)
        if output is None:
            # TODO: Should this return None?
            return False
        components = output.split()
        return components[1] == '-'

    @classmethod
    def is_lfs_file_not_pointer(cls, path: Path, file: str) -> bool:
        output = cmd.get_stdout(f'git lfs ls-files -I "{file}"', cwd=path)
        if output is None:
            # TODO: Should this return None?
            return False
        components = output.split()
        return components[1] == '*'

    @classmethod
    def get_git_config(cls, path: Path) -> Optional[str]:
        return cmd.get_stdout('git config --list --show-origin', cwd=path)

    @classmethod
    def stash(cls, path: Path) -> CompletedProcess:
        return cmd.run('git stash', cwd=path)

    @classmethod
    def status(cls, path: Path, verbose: bool = False) -> CompletedProcess:
        args = ''
        if verbose:
            args = ' -vv '
        return cmd.run(f'git status {args}', cwd=path)

    @classmethod
    def current_head_commit_sha(cls, path: Path, short: bool = False) -> Optional[str]:
        args = ''
        if short:
            args = ' --short '
        return cmd.get_stdout(f'git rev-parse {args} {HEAD}', cwd=path)

    @classmethod
    def get_branch_sha(cls, path: Path, branch: str, remote: Optional[str] = None,
                       short: bool = False) -> Optional[str]:
        branch = branch if remote is None else f'{remote}/{branch}'
        return GitOffline.get_sha(path, ref=branch, short=short)

    @classmethod
    def add(cls, path: Path, files: List[str]) -> CompletedProcess:
        files = " ".join(files)
        return cmd.run(f"git add {files}", cwd=path)

    @classmethod
    def commit(cls, path: Path, message: str) -> CompletedProcess:
        return cmd.run(f"git commit -m '{message}'", cwd=path)

    @classmethod
    def create_local_branch(cls, path: Path, name: str, branch: Optional[str] = None,
                            remote: Optional[str] = None, track: bool = True) -> CompletedProcess:
        remote = '' if remote is None else f'{remote}/'
        start_point = HEAD if branch is None else f'{remote}{branch}'

        # TODO: Use a list for args and join with ' '
        args = ''
        if track:
            args += ' --track '
        else:
            args += ' --no-track '
        return cmd.run(f"git branch {args} {name} {start_point}", cwd=path)

    @classmethod
    def delete_local_branch(cls, path: Path, branch: str, force: bool = False) -> CompletedProcess:
        args = ''
        if force:
            args += ' --force '
        return cmd.run(f'git branch --delete {args} {branch}', cwd=path)

    @classmethod
    def delete_local_tag(cls, path: Path, name: str) -> CompletedProcess:
        return cmd.run(f'git tag --delete {name}', cwd=path)

    @classmethod
    def check_ref_format(cls, refname: str) -> bool:
        """Check git ref format

        :param str refname: Files to git add
        """

        result = cmd.run_silent(f'git check-ref-format --normalize {refname}')
        return result.returncode == 0

    @classmethod
    def reset_timestamp(cls, path: Path, timestamp: str, ref: str, author: Optional[str] = None) -> CompletedProcess:
        """Reset branch to upstream or checkout tag/sha as detached HEAD

        :param Path path: Path to git repo
        :param str timestamp: Commit ref timestamp
        :param Optional[str] author: Commit author
        :param str ref: Reference ref
        :raise ClowderGitError:
        """

        rev = GitOffline.find_rev_by_timestamp(path, timestamp, ref, author=author)
        return GitOffline.checkout(path, rev)

    @classmethod
    def submodule_add(cls, path: Path, url: str, branch: Optional[str] = None, force: bool = False,
                      name: Optional[str] = None, reference: Optional[str] = None, depth: Optional[int] = None,
                      submodule_path: Optional[Path] = None) -> CompletedProcess:
        args = ''
        if branch is not None:
            args += f' -b {branch} '
        if force:
            args += ' --force '
        if name is not None:
            args += f' --name {name} '
        if reference is not None:
            args += f' --reference {reference} '
        if depth is not None:
            args += f' --depth {depth} '
        if submodule_path is not None:
            submodule_path = str(submodule_path)
        else:
            submodule_path = ''
        return cmd.run(f'git submodule add {args} {url} {submodule_path}', cwd=path)

    @classmethod
    def submodule_absorbgitdirs(cls, path: Path, paths: Optional[List[Path]] = None) -> CompletedProcess:
        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ''
        return cmd.run(f'git submodule absorbgitdirs {paths}', cwd=path)

    @classmethod
    def submodule_foreach_clean(cls, path: Path, recursive: bool = False) -> CompletedProcess:
        return GitOffline.submodule_foreach(path, 'git clean -ffdx', recursive=recursive)

    @classmethod
    def submodule_foreach_reset(cls, path: Path, recursive: bool = False, hard: bool = False) -> CompletedProcess:
        args = ''
        if hard:
            args += ' --hard '
        return GitOffline.submodule_foreach(path, f'git reset {args}', recursive=recursive)

    @classmethod
    def submodule_foreach(cls, path: Path, command: str, recursive: bool = False) -> CompletedProcess:
        args = ''
        if recursive:
            args += ' --recursive '
        return cmd.run(f'git submodule foreach {args} {command}', cwd=path)

    @classmethod
    def submodule_sync(cls, path: Path, recursive: bool = False,
                       paths: Optional[List[Path]] = None) -> CompletedProcess:
        args = ''
        if recursive:
            args += ' --recursive '
        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ''
        return cmd.run(f'git submodule sync {args} {paths}', cwd=path)

    @classmethod
    def submodule_deinit(cls, path: Path, force: bool = False, paths: Optional[List[Path]] = None) -> CompletedProcess:
        args = ''
        if force:
            args += ' --force '
        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ' --all '
        return cmd.run(f'git submodule deinit {args} {paths}', cwd=path)

    @classmethod
    def submodule_init(cls, path: Path, paths: Optional[List[Path]] = None) -> CompletedProcess:
        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ''
        return cmd.run(f'git submodule init {paths}', cwd=path)

    @classmethod
    def submodule_set_branch(cls, path: Path, submodule_path: Path, branch: str) -> CompletedProcess:
        return cmd.run(f'git submodule set-url --branch {branch} {submodule_path}', cwd=path)

    @classmethod
    def submodule_unset_branch(cls, path: Path, submodule_path: Path) -> CompletedProcess:
        return cmd.run(f'git submodule set-url --default {submodule_path}', cwd=path)

    @classmethod
    def submodule_set_url(cls, path: Path, submodule_path: Path, url: str) -> CompletedProcess:
        return cmd.run(f'git submodule set-url {submodule_path} {url}', cwd=path)

    @classmethod
    def submodule_status(cls, path: Path, cached: bool = False, recursive: bool = False,
                         paths: Optional[List[Path]] = None) -> CompletedProcess:
        args = ''
        if cached:
            args += ' --cached '
        if recursive:
            args += ' -- recursive '
        if paths is not None and paths:
            paths = ' '.join([str(p) for p in paths])
        else:
            paths = ''
        return cmd.run(f'git submodule status {args} {paths}', cwd=path)

    @classmethod
    def has_ignored_files(cls, path: Path) -> bool:
        ignored_files = GitOffline.check_ignore(path)
        return bool(ignored_files)

    @classmethod
    def check_ignore(cls, path: Path) -> List[str]:
        output = cmd.get_stdout('git check-ignore -v *', cwd=path)
        if output is None:
            return []
        # TODO: Process output
        # Expected output:
        # .gitignore:1:ignored_file	ignored_file
        return output.splitlines()

    @classmethod
    def clean(cls, path: Path, untracked_directories: bool = False, force: bool = False,
              ignored: bool = False, untracked_files: bool = False) -> CompletedProcess:
        """Discard changes for repo

        :param Path path: Path to git repo
        :param bool untracked_directories: ``d`` Remove untracked directories in addition to untracked files
        :param bool force: ``f`` Delete directories with .git sub directory or file
        :param bool ignored: ``X`` Remove only files ignored by git
        :param bool untracked_files: ``x`` Remove all untracked files
        """

        args = '-f'
        if untracked_directories:
            args += 'd'
        if force:
            args += 'f'
        if ignored:
            args += 'X'
        if untracked_files:
            args += 'x'
        return cmd.run(f"git clean {args}", cwd=path)

    @classmethod
    def checkout(cls, path: Path, ref: str, track: bool = False) -> CompletedProcess:
        track = ' --track ' if track else ''
        return cmd.run(f"git -c advice.detachedHead=false checkout {track} {ref}", cwd=path)

    @classmethod
    def local_branch_exists(cls, path: Path, branch: str) -> bool:
        result = cmd.run_silent(f"git rev-parse --quiet --verify refs/heads/{branch}", cwd=path)
        return result.returncode == 0

    @classmethod
    def get_tracking_branches_info(cls, path: Path) -> Dict[str, Dict[str, str]]:
        local_branches = GitOffline.get_local_branches_info(path)
        upstream_branches = {}
        for branch in local_branches:
            upstream_branch = GitOffline.get_upstream_branch(path, branch)
            push_branch_info = GitOffline.get_push_branch(path, branch)
            push_branch = None if push_branch_info is None else push_branch_info[0]
            push_remote = None if push_branch_info is None else push_branch_info[1]
            if upstream_branch is not None:
                upstream_branches[branch] = {
                    'upstream_branch': upstream_branch[0],
                    'upstream_remote': upstream_branch[1],
                    'push_branch': push_branch,
                    'push_remote': push_remote
                }
        return upstream_branches

    @classmethod
    def get_upstream_branch(cls, path: Path, branch: str) -> Optional[Tuple[str, Optional[str]]]:
        return GitOffline.rev_parse_tracking_branch(path, branch, 'upstream')

    @classmethod
    def get_push_branch(cls, path: Path, branch: str) -> Optional[Tuple[str, Optional[str]]]:
        return GitOffline.rev_parse_tracking_branch(path, branch, 'push')

    @classmethod
    def rev_parse_tracking_branch(cls, path: Path, branch: str, arg: str) -> Optional[Tuple[str, Optional[str]]]:
        output = cmd.get_stdout(f'git rev-parse --symbolic-full-name {branch}@{{{arg}}}', cwd=path)
        if output is None:
            return None
        return ProcessOutput.tracking_branches(output)

    @classmethod
    def get_full_branch_ref(cls, path: Path, branch: str) -> Optional[str]:
        return cmd.get_stdout(f'git rev-parse --symbolic-full-name {branch}', cwd=path)

    @classmethod
    def git_remote_show(cls, path: Path, remote: str) -> Optional[str]:
        return cmd.get_stdout(f'git remote show {remote}', cwd=path)

    @classmethod
    def has_tracking_branch(cls, path: Path, branch: str) -> bool:
        result = cmd.run_silent(f'git config --get branch.{branch}.merge', cwd=path)
        return result.returncode == 0

    @classmethod
    def check_remote_url(cls, path: Path, remote, url) -> bool:
        output = cmd.get_stdout(f"git remote get-url {remote}", cwd=path)
        if output is None:
            # TODO: Should this return None?
            return False
        return output == url

    @classmethod
    def is_on_branch(cls, path: Path, branch: str) -> bool:
        return GitOffline.current_branch(path) == branch

    @classmethod
    def current_branch(cls, path: Path) -> Optional[str]:
        branch = cmd.get_stdout(f'git rev-parse --abbrev-ref {HEAD}', cwd=path)
        if branch is None:
            return None
        return Format.remove_prefix(branch, 'heads/')

    @classmethod
    def set_upstream_branch(cls, path: Path, local_branch: str, upstream_branch: str,
                            remote: Optional[str] = None) -> CompletedProcess:
        remote_arg = ''
        if remote is not None:
            remote_arg = f'{remote}/'

        return cmd.run(f'git branch --set-upstream-to={remote_arg}{upstream_branch} {local_branch}', cwd=path)

    @classmethod
    def git_config_unset_all_local(cls, path: Path, variable: str) -> CompletedProcess:
        """Unset all local git config values for given variable key

        :param Path path: Path to git repo
        :param str variable: Fully qualified git config variable
        """

        try:
            return cmd.run(f'git config --local --unset-all {variable}', cwd=path)
        except CalledProcessError as err:
            # git returns error code 5 when trying to unset variable that doesn't exist
            if err.returncode != 5:
                raise

    @classmethod
    def git_config_add_local(cls, path: Path, variable: str, value: str) -> CompletedProcess:
        """Add local git config value for given variable key

        :param Path path: Path to git repo
        :param str variable: Fully qualified git config variable
        :param str value: Git config value
        """

        # TODO: Use Python ConfigParser for this
        return cmd.run(f'git config --local --add "{variable}" "{value}"', cwd=path)

    @classmethod
    def is_detached(cls, path: Path) -> bool:
        return GitOffline.current_branch(path) == HEAD

    @classmethod
    def get_tag_commit_sha(cls, path: Path, tag: str) -> Optional[str]:
        return cmd.get_stdout(f'git rev-list -n 1 {tag}', cwd=path)

    @classmethod
    def get_sha(cls, path: Path, ref: str = HEAD, short: bool = False) -> Optional[str]:
        args = ''
        if short:
            args = ' --short '
        return cmd.get_stdout(f'git rev-parse {args} {ref}', cwd=path)

    @classmethod
    def number_of_commits_between_refs(cls, path: Path, first: str, second: str) -> int:
        output = cmd.get_stdout(f"git rev-list {first}..{second} --count", cwd=path)
        if output is None:
            # TODO: Should this return None?
            return 0
        return int(output)

    @classmethod
    def reset(cls, path: Path, ref: str = HEAD, hard: bool = False, mixed: bool = False,
              soft: bool = False, merge: bool = False, keep: bool = False) -> CompletedProcess:
        args = ''
        if sum([hard, mixed, soft, merge, keep]) > 1:
            raise Exception('Only one of args hard, mixed, soft, merge, keep allowed to be true')
        if hard:
            args = ' --hard '
        if mixed:
            args = ' --mixed '
        if soft:
            args = ' --soft '
        if merge:
            args = ' --merge '
        if keep:
            args = ' --keep '
        return cmd.run(f"git reset {args} {ref}", cwd=path)

    @classmethod
    def reset_back(cls, path: Path, number: int) -> CompletedProcess:
        sha = GitOffline.current_head_commit_sha(path)
        result = cmd.run(f"git reset --hard {HEAD}~{number}", cwd=path)
        assert GitOffline.number_of_commits_between_refs(path, HEAD, sha) == number
        return result

    @classmethod
    def has_no_commits_between_refs(cls, path: Path, start: str, end: str) -> bool:
        result_1 = GitOffline.number_of_commits_between_refs(path, start, end) == 0
        result_2 = GitOffline.number_of_commits_between_refs(path, end, start) == 0
        return result_1 and result_2

    @classmethod
    def is_ahead_by_number_commits(cls, path: Path, start: str, end: str, number_commits: int) -> bool:
        return GitOffline.number_commits_ahead(path, start, end) == number_commits

    @classmethod
    def is_behind_by_number_commits(cls, path: Path, start: str, end: str, number_commits: int) -> bool:
        return GitOffline.number_commits_behind(path, start, end) == number_commits

    @classmethod
    def number_commits_ahead(cls, path: Path, start: str, end: str) -> int:
        return GitOffline.number_of_commits_between_refs(path, end, start)

    @classmethod
    def number_commits_behind(cls, path: Path, start: str, end: str) -> int:
        return GitOffline.number_of_commits_between_refs(path, start, end)

    @classmethod
    def abort_rebase(cls, path: Path) -> CompletedProcess:
        return cmd.run('git rebase --abort', cwd=path)

    @classmethod
    def get_commit_messages_behind(cls, path: Path, ref: str, count: int = 1) -> List[str]:
        results = []
        commit_number = 0
        while commit_number < count:
            result = GitOffline.get_commit_message(path, f"{ref}~{commit_number}")
            results.append(result)
            commit_number += 1
        return results

    @classmethod
    def get_commit_message(cls, path: Path, ref: str) -> Optional[str]:
        return cmd.get_stdout(f"git log --format=%B -n 1 {ref}", cwd=path)

    @classmethod
    def is_shallow_repo(cls, path: Path) -> bool:
        output = cmd.get_stdout("git rev-parse --is-shallow-repository", cwd=path)
        if output is None:
            # TODO: Should this return None?
            return False
        return output == "true"

    @classmethod
    def get_remote_branches_info(cls, path: Path, remote: str) -> Tuple[List[str], Optional[str]]:
        output = cmd.get_stdout('git branch -r', cwd=path)
        if output is None:
            return [], None
        return ProcessOutput.remote_branches(output, remote=remote)

    @classmethod
    def get_commit_date(cls, path: Path, commit: str) -> Optional[datetime]:
        output = cmd.get_stdout(f'git show -s --format=%ci {commit}', cwd=path)
        if output is None:
            return None
        date = datetime.strptime(output, '%Y-%m-%d %H:%M:%S %z')
        return date
