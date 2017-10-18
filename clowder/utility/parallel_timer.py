"""Git utilities"""

from tqdm import tqdm


class ClowderParallelProgress(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_progress(self):
        """Updates progress bar for each invacation"""
        self.update(self.n + 1)
