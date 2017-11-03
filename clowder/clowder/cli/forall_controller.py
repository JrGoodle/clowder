from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class ForallController(AbstractBaseController):
    class Meta:
        label = 'forall'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run command or script in project directories'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--command', '-c'], dict(nargs=1, metavar='COMMAND',
                                       help='command or script to run in project directories')),
            (['--ignore-errors', '-i'], dict(action='store_true', help='ignore errors in command or script')),
            (['--parallel'], dict(action='store_true', help='run commands in parallel'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
