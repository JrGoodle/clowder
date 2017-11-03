import os
import sys

from cement.ext.ext_argparse import expose

from clowder.clowder_controller import ClowderController
from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.cli.util import (
    fork_project_names,
    options_help_message
)


class SyncController(AbstractBaseController):
    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Sync fork with upstream remote'
        clowder = None
        try:
            clowder = ClowderController(os.getcwd())
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except:
            pass
        finally:
            project_names = fork_project_names(clowder)
            projects_help = options_help_message(project_names, 'projects to sync')
            arguments = [
                (['--projects', '-p'], dict(choices=project_names, nargs='+', metavar='PROJECT', help=projects_help)),
                (['--rebase', '-r'], dict(action='store_true', help='use rebase instead of pull')),
                (['--parallel'], dict(action='store_true', help='run commands in parallel'))
                ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")

