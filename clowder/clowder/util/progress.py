# -*- coding: utf-8 -*-
"""Progress bar

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from tqdm import tqdm


class Progress(object):
    """Class wrapping progress bar"""

    def __init__(self):
        self._bar = None

    def close(self):
        """Close progress bar

        :return:
        """

        if self._bar:
            self._bar.close()

    def complete(self):
        """Complete progress bar

        :return:
        """

        if self._bar:
            if self._bar.n < self._bar.total:
                self._bar.n = self._bar.total

    def start(self, count):
        """Start progress bar

        :param int count: Initial count
        :return:
        """

        if self._bar:
            self._bar.close()

        bar_format = '{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} projects'
        self._bar = tqdm(total=count, unit='projects', bar_format=bar_format)

    def update(self):
        """Update progress bar

        :return:
        """

        if self._bar:
            self._bar.update()
