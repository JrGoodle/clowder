from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class BranchController(AbstractBaseController):
    class Meta:
        label = 'branch'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Display current branches'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
