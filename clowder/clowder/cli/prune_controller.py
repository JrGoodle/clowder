from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class PruneController(AbstractBaseController):
    class Meta:
        label = 'prune'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Prune branches'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--force', '-f'], dict(action='store_true', help='force prune branches')),
            (['branch'], dict(help='name of branch to remove', metavar='BRANCH')),
            (['--all', '-a'], dict(action='store_true', help='prune local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='prune remote branches'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
