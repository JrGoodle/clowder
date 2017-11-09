# -*- coding: utf-8 -*-
"""Clowder exit exception

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""


class ClowderExit(Exception):
    """Clowder exit error type"""

    def __init__(self, code):
        """ClowderExit __init__

        :param int code: Exit code
        """

        super(ClowderExit, self).__init__(code)
        self.code = code
