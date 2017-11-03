from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class StatusController(AbstractBaseController):
    class Meta:
        label = 'status'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Print project status'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--fetch', '-f'], dict(action='store_true', help='fetch projects before printing status'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
