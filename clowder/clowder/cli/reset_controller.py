import os
import sys

from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.cli.util import project_names
from clowder.clowder_controller import ClowderController


class ResetController(AbstractBaseController):
    class Meta:
        label = 'reset'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'

        clowder = None
        try:
            clowder = ClowderController(os.getcwd())
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except:
            pass
        finally:
            project_names = project_names(clowder)
            arguments = AbstractBaseController.Meta.arguments + [
                (['--parallel'], dict(action='store_true', help='run commands in parallel')),
                (['--timestamp', '-t'], dict(choices=project_names, default=None, nargs=1, metavar='TIMESTAMP',
                                             help='project to reset timestamps relative to'))
                ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
