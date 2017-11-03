from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class StashController(AbstractBaseController):
    class Meta:
        label = 'stash'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Stash current changes'

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
