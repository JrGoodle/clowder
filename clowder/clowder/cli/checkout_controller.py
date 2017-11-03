from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class CheckoutController(AbstractBaseController):
    class Meta:
        label = 'checkout'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Checkout local branch in projects'
        arguments = AbstractBaseController.Meta.arguments + [
            (['branch'], dict(help='branch to checkout', metavar='BRANCH'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
