"""Clowder cli __init__.py"""

import sys

from clowder.cli.base_controller import BaseController
from clowder.cli.branch_controller import BranchController
from clowder.cli.checkout_controller import CheckoutController
from clowder.cli.clean_controller import CleanController
from clowder.cli.diff_controller import DiffController
from clowder.cli.forall_controller import ForallController
from clowder.cli.herd_controller import HerdController
from clowder.cli.init_controller import InitController
from clowder.cli.link_controller import LinkController
from clowder.cli.prune_controller import PruneController
from clowder.cli.repo_controller import (
    RepoController,
    RepoAddController,
    RepoCommitController,
    RepoRunController,
    RepoPullController,
    RepoPushController
)
from clowder.cli.reset_controller import ResetController
from clowder.cli.save_controller import SaveController
from clowder.cli.start_controller import StartController
from clowder.cli.stash_controller import StashController
from clowder.cli.status_controller import StatusController
from clowder.cli.sync_controller import SyncController
from clowder.cli.yaml_controller import YAMLController

if sys.version_info[0] >= 3:
    from clowder.cli.repo_controller import (
        RepoCheckoutController,
        RepoCleanController,
        RepoStatusController
    )
