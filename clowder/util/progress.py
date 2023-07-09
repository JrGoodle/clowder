"""progress utilities

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from threading import Lock
from typing import Any, Dict, Optional

from rich.console import Console
from rich.progress import TaskID, BarColumn, ProgressColumn, Task
from rich.progress import Progress as RichProgress

from .format import Format
from .console import CONSOLE


class DownloadProgressColumn(ProgressColumn):

    def __init__(self) -> None:
        super().__init__()
        self._width: int = 0

    def render(self, task: Task) -> str:
        if 'units' in task.fields and task.fields['units'] == 'bytes':
            downloaded = Format.gnu_size(int(task.completed))
            total = Format.gnu_size(int(task.total))
            output = f'{downloaded}/{total}'
        else:
            output = f'{task.completed}/{task.total}'

        width = max(self._width, len(output))
        if width > self._width:
            self._width = width
        return output.rjust(self._width)


class Progress:

    def __init__(self, console: Optional[Console] = None, should_clear_lines: bool = True):
        self._delete_line_count: int = 0
        self._lock: Lock = Lock()
        self._task_ids: Dict[str: TaskID] = {}
        self._subtask_ids: Dict[str: TaskID] = {}
        self._should_clear_lines: bool = should_clear_lines

        self._progress_bar_format = [
            "[progress.description]{task.description}",
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadProgressColumn(),
            "{task.fields[units]}"
        ]
        self._progress: RichProgress = RichProgress(*self._progress_bar_format, console=console)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def add_task(self, identifier: Any, total: int, units: str, start: bool = True) -> None:
        task_id = self._progress.add_task(str(identifier), total=total, units=units, start=start)
        self._add_task_id(identifier, task_id)

    def add_subtask(self, identifier: Any, total: int, units: str, start: bool = True) -> None:
        task_id = self._progress.add_task(str(identifier), total=total, units=units, start=start)
        self._add_subtask_id(identifier, task_id)
        count = len(self._progress.tasks)
        if count <= 1:
            return
        with self._lock:
            self._delete_line_count = max(self._delete_line_count, count - 1)

    def clear_lines(self) -> None:
        if self._should_clear_lines:
            CONSOLE.delete_lines(count=self._delete_line_count, force=True)

    def complete_task(self, identifier: Any) -> None:
        task_id = self._get_task_id(identifier)
        task = self._progress.tasks[task_id]
        self._progress.update(task_id, completed=task.total)

    def complete_subtask(self, identifier: Any) -> None:
        task_id = self._get_subtask_id(identifier)
        # task = self._progress.tasks[task_id]
        # self._progress.update(task_id, completed=task.total, visible=False)
        self._progress.remove_task(task_id)

    def start(self) -> None:
        self._progress.start()

    def start_task(self, identifier: Any) -> None:
        task_id = self._get_task_id(identifier)
        self._progress.start_task(task_id)

    def start_subtask(self, identifier: Any) -> None:
        task_id = self._get_subtask_id(identifier)
        self._progress.start_task(task_id)

    def stop(self, clear_lines: bool = True) -> None:
        self._progress.stop()
        if clear_lines:
            self.clear_lines()

    def update_task(self, identifier: Any, advance: int) -> None:
        task_id = self._get_task_id(identifier)
        self._progress.update(task_id, advance=advance)

    def update_subtask(self, identifier: Any, advance: int) -> None:
        task_id = self._get_subtask_id(identifier)
        self._progress.update(task_id, advance=advance)

    def _get_task_id(self, identifier: Any) -> TaskID:
        return self._task_ids[str(identifier)]

    def _get_subtask_id(self, identifier: Any) -> TaskID:
        return self._subtask_ids[str(identifier)]

    def _add_task_id(self, identifier: Any, task_id: TaskID) -> None:
        with self._lock:
            self._task_ids[str(identifier)] = task_id

    def _add_subtask_id(self, identifier: Any, task_id: TaskID) -> None:
        with self._lock:
            self._subtask_ids[str(identifier)] = task_id
