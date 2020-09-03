# -*- coding: utf-8 -*-
"""Progress bar wrapper class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

# noinspection PyPackageRequirements
from tqdm import tqdm


class Progress(object):
    """Class wrapping progress bar"""

    def __init__(self):
        self._bar = None

    def close(self) -> None:
        """Close progress bar"""

        if self._bar:
            self._bar.close()

    def complete(self) -> None:
        """Complete progress bar"""

        if self._bar and self._bar.n < self._bar.total:
            self._bar.n = self._bar.total

    def start(self, count: int) -> None:
        """Start progress bar

        :param int count: Initial count
        """

        if self._bar:
            self._bar.close()

        bar_format = '{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} projects'
        self._bar = tqdm(total=count, unit='projects', bar_format=bar_format)

    def update(self) -> None:
        """Update progress bar"""

        if self._bar:
            self._bar.update()
