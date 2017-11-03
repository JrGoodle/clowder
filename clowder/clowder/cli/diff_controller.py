from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class DiffController(AbstractBaseController):
    class Meta:
        label = 'diff'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Show git diff for projects'

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
