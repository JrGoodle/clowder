"""Clowder parallel commands

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import partial
from typing import Callable, Optional, Tuple

from pygoodle.console import CONSOLE
from pygoodle.formatting import Format
from pygoodle.tasks import ProgressTask, ProgressTaskPool
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.data import ResolvedProject


class ForallTask(ProgressTask):
    def __init__(self, project: ResolvedProject, func: str, **kwargs):
        project_func = getattr(project, func)
        self._func: Callable = partial(project_func, **kwargs)
        super().__init__(str(project.path))

    def run(self) -> None:
        self._func()


def forall(projects: Tuple[ResolvedProject, ...], jobs: int, command: str, ignore_errors: bool) -> None:
    """Runs command or script for projects in parallel

    :param Tuple[ResolvedProject, ...] projects: Projects to run command for
    :param int jobs: Number of jobs to use running parallel commands
    :param str command: Command to run
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    """

    CONSOLE.stdout(' - Run forall commands in parallel\n')
    for project in projects:
        CONSOLE.stdout(project.status())
        if not project.full_path.is_dir():
            CONSOLE.stdout(Format.red(" - Project missing"))

    tasks = [ForallTask(p, 'run', command=command, ignore_errors=ignore_errors) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)


def herd(projects: Tuple[ResolvedProject, ...], jobs: int, branch: Optional[str] = None,
         tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False) -> None:
    """Clone projects or update latest from upstream in parallel

    :param Tuple[ResolvedProject, ...] projects: Projects to herd
    :param int jobs: Number of jobs to use running parallel commands
    :param Optional[str] branch: Branch to attempt to herd
    :param Optional[str] tag: Tag to attempt to herd
    :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    CONSOLE.stdout(' - Herd projects in parallel\n')
    CLOWDER_CONTROLLER.validate_print_output(projects)

    tasks = [ForallTask(p, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)


def reset(projects: Tuple[ResolvedProject, ...], jobs: int, timestamp_project: Optional[str] = None) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

    :param Tuple[ResolvedProject, ...] projects: Project names to reset
    :param int jobs: Number of jobs to use running parallel commands
    :param Optional[str] timestamp_project: Reference project to checkout other project timestamps relative to
    """

    CONSOLE.stdout(' - Reset projects in parallel\n')
    CLOWDER_CONTROLLER.validate_print_output(projects)

    timestamp = None
    if timestamp_project:
        timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

    tasks = [ForallTask(p, 'reset', timestamp=timestamp) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)
