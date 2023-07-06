"""Clowder parallel commands

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import partial
from typing import Callable, Iterable, List, Optional, Union

from clowder.util.console import CONSOLE
from clowder.util.format import Format
from clowder.util.tasks import ProgressTask, ProgressTaskPool, Task, TaskPool
from clowder.controller import CLOWDER_CONTROLLER, ClowderRepo, ProjectRepo


class ForallTask(ProgressTask):
    def __init__(self, project: ProjectRepo, func: str, **kwargs):
        project_func = getattr(project, func)
        self._func: Callable = partial(project_func, **kwargs)
        super().__init__(str(project.path), start=False)

    def run(self) -> None:
        self._func()


def forall(projects: Iterable[ProjectRepo], jobs: int, command: str, check: bool) -> None:
    """Runs command or script for projects in parallel

    :param Iterable[ProjectRepo] projects: Projects to run command for
    :param int jobs: Number of jobs to use running parallel commands
    :param str command: Command to run
    :param bool check: Whether to exit if command returns a non-zero exit code
    """

    CONSOLE.stdout(' - Run forall commands in parallel\n')
    for project in projects:
        CONSOLE.stdout(project.status())
        if not project.path.is_dir():
            CONSOLE.stdout(Format.red(" - Project missing"))

    tasks = [ForallTask(p, 'run', command=command, check=check) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)


def herd(projects: Iterable[ProjectRepo], jobs: int, branch: Optional[str] = None,
         tag: Optional[str] = None, depth: Optional[int] = None, rebase: bool = False) -> None:
    """Clone projects or update latest from upstream in parallel

    :param Iterable[ProjectRepo] projects: Projects to herd
    :param int jobs: Number of jobs to use running parallel commands
    :param Optional[str] branch: Branch to attempt to herd
    :param Optional[str] tag: Tag to attempt to herd
    :param Optional[int] depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
    :param bool rebase: Whether to use rebase instead of pulling latest changes
    """

    CONSOLE.stdout(' - Herd projects in parallel\n')
    CLOWDER_CONTROLLER.validate_projects_state(projects)

    tasks = [ForallTask(p, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)


def reset(projects: Iterable[ProjectRepo], jobs: int, timestamp_project: Optional[str] = None) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

    :param Iterable[ProjectRepo] projects: Project names to reset
    :param int jobs: Number of jobs to use running parallel commands
    :param Optional[str] timestamp_project: Reference project to checkout other project timestamps relative to
    """

    CONSOLE.stdout(' - Reset projects in parallel\n')
    CLOWDER_CONTROLLER.validate_projects_state(projects)

    timestamp = None
    if timestamp_project:
        timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

    tasks = [ForallTask(p, 'reset', timestamp=timestamp) for p in projects]
    pool = ProgressTaskPool(jobs=jobs, title='Projects')
    pool.run(tasks)


def status(projects: Iterable[ProjectRepo], padding: int) -> List[str]:

    class StatusTask(Task):
        def __init__(self, project: ProjectRepo):
            super().__init__(str(id(project)))
            self._project: ProjectRepo = project

        def run(self) -> str:
            return self._project.status(padding=padding)

    tasks = [StatusTask(p) for p in projects]
    results = TaskPool().run(tasks)
    return results


def fetch(projects: Iterable[ProjectRepo], clowder_repo: Optional[ClowderRepo]) -> None:

    class FetchTask(ProgressTask):
        def __init__(self, repo: Union[ProjectRepo, ClowderRepo]):
            super().__init__(str(id(repo)))
            self._repo: Union[ProjectRepo, ClowderRepo] = repo

        def run(self) -> None:
            self._repo.fetch()

    tasks = [FetchTask(p) for p in projects]
    if clowder_repo is not None:
        tasks = [FetchTask(clowder_repo)] + tasks
    ProgressTaskPool(title='Fetch repos', print_subprogress=False, units='repos').run(tasks)
