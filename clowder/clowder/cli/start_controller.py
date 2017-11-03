from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class StartController(AbstractBaseController):
    class Meta:
        label = 'start'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Start a new branch'
        arguments = AbstractBaseController.Meta.arguments + [
            (['branch'], dict(help='name of branch to create', metavar='BRANCH')),
            (['--tracking', '-t'], dict(action='store_true', help='create remote tracking branch'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
