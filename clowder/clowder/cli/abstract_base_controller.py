import os
import sys

from cement.ext.ext_argparse import ArgparseController, expose
from termcolor import cprint

from clowder.error.clowder_error import ClowderError
from clowder.cli.util import (
    group_names,
    project_names
)
from clowder.clowder_controller import ClowderController
from clowder.clowder_repo import ClowderRepo


class AbstractBaseController(ArgparseController):
    """
    This is an abstract base class that is useless on its own, but used
    by other classes to sub-class from and to share common commands and
    arguments.  This should not be confused with the `MyAppBaseController`
    used as the ``base_controller`` namespace.

    """
    class Meta:
        stacked_on = 'base'
        stacked_type = 'nested'

        clowder = None
        try:
            clowder = ClowderController(os.getcwd())
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        except:
            pass
        finally:
            group_names = group_names(clowder)
            project_names = project_names(clowder)
            arguments = [
                (['--groups', '-g'], dict(choices=group_names, default=group_names, nargs='+', metavar='GROUP',
                                          help='groups to herd')),
                (['--projects', '-p'], dict(choices=project_names, nargs='+', metavar='PROJECT',
                                            help='projects to herd')),
                (['--skip', '-s'], dict(choices=project_names, nargs='+', metavar='PROJECT', default=[],
                                        help='projects to skip'))
                ]

    def _setup(self, base_app):
        super(AbstractBaseController, self)._setup(base_app)

        self.root_directory = os.getcwd()
        self.clowder = None
        self.clowder_repo = None
        self.versions = None
        self.invalid_yaml = False
        clowder_path = os.path.join(self.root_directory, '.clowder')

        # Load current clowder.yaml config if it exists
        if os.path.isdir(clowder_path):
            clowder_symlink = os.path.join(self.root_directory, 'clowder.yaml')
            self.clowder_repo = ClowderRepo(self.root_directory)
            if not os.path.islink(clowder_symlink):
                cprint('\n.clowder', 'green')
                self.clowder_repo.link()
            try:
                self.clowder = ClowderController(self.root_directory)
            except (ClowderError, KeyError) as err:
                self.invalid_yaml = True
                self.error = err
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

    @expose(hide=True)
    def default(self):
        """
        This command will be shared within all controllers that sub-class
        from here.  It can also be overridden in the sub-class, but for
        this example we are making it dynamic.

        """
        # # do something with self.my_shared_obj here?
        # if 'some_key' in self.reusable_dict.keys():
        #     pass

        print(self.root_directory)
        print(self.clowder_repo.default_ref)
        print(self.clowder.groups)

        # or do something with parsed args?
        # if self.app.pargs.groups:
        #     print("Groups option was passed with value: %s" % self.app.pargs.groups)

        # or maybe do something dynamically
        print("Inside %s.default()" % self.__class__.__name__)

