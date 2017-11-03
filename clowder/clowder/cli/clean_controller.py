from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController


class CleanController(AbstractBaseController):
    class Meta:
        label = 'clean'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Discard current changes in projects'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--all', '-a'], dict(action='store_true', help='clean all the things')),
            (['--recursive', '-r'], dict(action='store_true', help='clean submodules recursively')),
            (['-d'], dict(action='store_true', help='remove untracked directories')),
            (['-f'], dict(action='store_true', help='remove directories with .git subdirectory or file')),
            (['-X'], dict(action='store_true', help='remove only files ignored by git')),
            (['-x'], dict(action='store_true', help='remove all untracked files'))
            ]

    @expose(help="second-controller default command", hide=True)
    def default(self):
        print("Inside SecondController.default()")
