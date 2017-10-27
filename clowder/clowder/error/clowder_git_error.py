"""Clowder git exception"""


class ClowderGitError(Exception):
    """Clowder git error type"""

    def __init__(self, msg=None):
        super(ClowderGitError, self).__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg if isinstance(self.msg, str) else "ClowderGitException"
