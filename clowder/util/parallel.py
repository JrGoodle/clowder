"""Clowder parallel commands

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from functools import partial
from typing import Callable, Optional, Tuple

from tqdm import tqdm
import trio

import clowder.util.formatting as fmt
from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.console import CONSOLE
from clowder.data import ResolvedProject
from clowder.logging import LOG_DEBUG


def forall(projects: Tuple[ResolvedProject, ...], jobs: int, command: str, ignore_errors: bool) -> None:
    """Runs command or script for projects in parallel

    :param Tuple[ResolvedProject, ...] projects: Projects to run command for
    :param int jobs: Number of jobs to use running parallel commands
    :param str command: Command to run
    :param bool ignore_errors: Whether to exit if command returns a non-zero exit code
    """

    CONSOLE.print(' - Run forall commands in parallel\n')
    for project in projects:
        CONSOLE.print(project.status())
        if not project.full_path.is_dir():
            CONSOLE.print(fmt.red(" - Project missing"))

    forall_func = partial(run_parallel, jobs, projects, 'run', command=command, ignore_errors=ignore_errors)
    trio.run(forall_func)


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

    CONSOLE.print(' - Herd projects in parallel\n')
    CLOWDER_CONTROLLER.validate_print_output(projects)

    run_func = partial(run_parallel, jobs, projects, 'herd', branch=branch, tag=tag, depth=depth, rebase=rebase)
    trio.run(run_func)


def reset(projects: Tuple[ResolvedProject, ...], jobs: int, timestamp_project: Optional[str] = None) -> None:
    """Reset project branches to upstream or checkout tag/sha as detached HEAD in parallel

    :param Tuple[ResolvedProject, ...] projects: Project names to reset
    :param int jobs: Number of jobs to use running parallel commands
    :param Optional[str] timestamp_project: Reference project to checkout other project timestamps relative to
    """

    CONSOLE.print(' - Reset projects in parallel\n')
    CLOWDER_CONTROLLER.validate_print_output(projects)

    timestamp = None
    if timestamp_project:
        timestamp = CLOWDER_CONTROLLER.get_timestamp(timestamp_project)

    reset_func = partial(run_parallel, jobs, projects, 'reset', timestamp=timestamp)
    trio.run(reset_func)


async def run_parallel(jobs: int, projects: Tuple[ResolvedProject, ...], func_name: str, **kwargs) -> None:
    CONSOLE.print_output = False
    limit = trio.CapacityLimiter(jobs)
    unit = 'projects'
    base_bar_format = '{desc} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}'
    bar_format = f'{base_bar_format} {unit}'
    with tqdm(total=len(projects), desc=unit, unit=unit, bar_format=bar_format) as progress:
        async with trio.open_nursery() as nursery:
            for project in projects:
                await limit.acquire_on_behalf_of(project)
                func = getattr(project, func_name)
                project_func = partial(func, **kwargs, parallel=True)
                nursery.start_soon(run_sync, project_func, limit, project, progress)
    CONSOLE.print_output = True


async def run_sync(func: Callable, limit: trio.CapacityLimiter, project: ResolvedProject, progress: tqdm) -> None:
    LOG_DEBUG(f'START PARALLEL {project.name}')
    await trio.to_thread.run_sync(func, limiter=limit)
    limit.release_on_behalf_of(project)
    progress.update()
    LOG_DEBUG(f'END PARALLEL {project.name}')
