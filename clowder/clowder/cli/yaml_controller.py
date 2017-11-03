from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class YAMLController(AbstractBaseController):
    class Meta:
        label = 'yaml'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Print clowder.yaml information'
        arguments = [
            (['--resolved', '-r'], dict(action='store_true', help='print resolved clowder.yaml'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
