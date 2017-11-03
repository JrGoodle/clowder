from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command,
    validate_groups,
    validate_projects
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    network_connection_required,
    valid_clowder_yaml_required
)


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
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        if self.app.pargs.tracking:
            self._start_tracking()
            return

        if self.app.pargs.projects is None:
            _start_groups(self.clowder, self.app.pargs.groups, self.app.pargs.skip, self.app.pargs.branch)
        else:
            _start_projects(self.clowder, self.app.pargs.projects, self.app.pargs.skip, self.app.pargs.branch)

    @network_connection_required
    def _start_tracking(self):
        """clowder start tracking command"""

        if self.app.pargs.projects is None:
            _start_groups(self.clowder, self.app.pargs.groups, self.app.pargs.skip,
                          self.app.pargs.branch, tracking=True)
            return

        _start_projects(self.clowder, self.app.pargs.projects, self.app.pargs.skip,
                        self.app.pargs.branch, tracking=True)


def _start_groups(clowder, group_names, skip, branch, tracking=False):
    """Start feature branch for groups

    :param ClowderController clowder: ClowderController instance
    :param list[str] group_names: Group names to create branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    groups = filter_groups(clowder.groups, group_names)
    validate_groups(groups)
    for group in groups:
        run_group_command(group, skip, 'start', branch, tracking)


def _start_projects(clowder, project_names, skip, branch, tracking=False):
    """Start feature branch for projects

    :param ClowderController clowder: ClowderController instance
    :param list[str] project_names: Project names to creat branches for
    :param list[str] skip: Project names to skip
    :param str branch: Local branch name to create
    :param Optional[bool] tracking: Whether to create a remote branch with tracking relationship.
        Defaults to False
    """

    projects = filter_projects_on_project_names(clowder.groups, project_names)
    validate_projects(projects)
    for project in projects:
        run_project_command(project, skip, 'start', branch, tracking)
