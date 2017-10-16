"""Clowder git exception"""


class ClowderGitException(Exception):
    """Clowder git exception type"""
    def __init__(self, msg=None):
        super(ClowderGitException, self).__init__(msg)
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return "ClowderGitException"
        return self.msg
