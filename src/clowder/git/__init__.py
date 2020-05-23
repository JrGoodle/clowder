# -*- coding: utf-8 -*-
"""clowder.git module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from enum import Enum, unique

from .git_repo import GitRepo
from .project_repo import ProjectRepo
from .project_repo_recursive import ProjectRepoRecursive


@unique
class GitProtocol(Enum):
    """Git protocol enum"""

    SSH = "ssh"
    HTTPS = "https"
