"""pygoodle git module __init__

.. codeauthor:: Joe DeCapo <joe@polka.cat>

"""

from .constants import (
    GitConfig,
    HEAD,
    ORIGIN,
    FETCH_URL,
    PUSH_URL,
    GITMODULES
)

from .model.factory import AllBranches
from .model.branch.branch import Branch
from .model.commit import Commit
from .model.branch.local_branch import LocalBranch
from .model.tag.local_tag import LocalTag
from .model.protocol import Protocol
from .model.ref import Ref
from .model.remote import Remote
from .model.branch.remote_branch import RemoteBranch
from .model.tag.remote_tag import RemoteTag
from .model.repo import Repo
from .model.submodule import Submodule
from .model.tag.tag import Tag
from .model.branch.tracking_branch import TrackingBranch

from .offline import GitOffline
from .online import GitOnline
