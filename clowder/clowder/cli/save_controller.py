from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class SaveController(AbstractBaseController):
    class Meta:
        label = 'save'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Create version of clowder.yaml for current repos'
        arguments = [
            (['version'], dict(help='version to save', metavar='VERSION'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
