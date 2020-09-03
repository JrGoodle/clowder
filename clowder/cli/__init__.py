# -*- coding: utf-8 -*-
"""clowder.cli module __init__

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from clowder.cli.branch import add_branch_parser
from clowder.cli.checkout import add_checkout_parser
from clowder.cli.clean import add_clean_parser
from clowder.cli.config import add_config_parser
from clowder.cli.diff import add_diff_parser
from clowder.cli.forall import add_forall_parser
from clowder.cli.herd import add_herd_parser
from clowder.cli.init import add_init_parser
from clowder.cli.link import add_link_parser
from clowder.cli.prune import add_prune_parser
from clowder.cli.repo import add_repo_parser
from clowder.cli.reset import add_reset_parser
from clowder.cli.save import add_save_parser
from clowder.cli.start import add_start_parser
from clowder.cli.stash import add_stash_parser
from clowder.cli.status import add_status_parser
from clowder.cli.yaml import add_yaml_parser

from clowder.cli.util import add_parser_arguments
