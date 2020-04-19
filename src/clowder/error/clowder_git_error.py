# -*- coding: utf-8 -*-
"""Clowder git exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from typing import Optional


class ClowderGitError(Exception):
    """Clowder git error type"""

    def __init__(self, msg: Optional[str] = None):
        """ClowderGitError __init__

        :param Optional[str] msg: Error message
        """

        super(ClowderGitError, self).__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg if isinstance(self.msg, str) else "ClowderGitException"
