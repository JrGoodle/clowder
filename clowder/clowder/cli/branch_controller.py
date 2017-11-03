from cement.ext.ext_argparse import expose

from clowder.cli.abstract_base_controller import AbstractBaseController
from clowder.commands.util import (
    filter_groups,
    filter_projects_on_project_names,
    run_group_command,
    run_project_command
)
from clowder.util.decorators import (
    print_clowder_repo_status,
    valid_clowder_yaml_required
)


class BranchController(AbstractBaseController):
    class Meta:
        label = 'branch'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Display current branches'
        arguments = AbstractBaseController.Meta.arguments + [
            (['--all', '-a'], dict(action='store_true', help='show local and remote branches')),
            (['--remote', '-r'], dict(action='store_true', help='show remote branches'))
            ]

    @expose(help="second-controller default command", hide=True)
    @valid_clowder_yaml_required
    @print_clowder_repo_status
    def default(self):
        local = True
        remote = False
        if self.app.pargs.all:
            local = True
            remote = True
        elif self.app.pargs.remote:
            remote = True

        if self.app.pargs.projects is None:
            groups = filter_groups(self.clowder.groups, self.app.pargs.groups)
            for group in groups:
                run_group_command(group, self.app.pargs.skip, 'branch', local=local, remote=remote)
            return

        projects = filter_projects_on_project_names(self.clowder.groups, self.app.pargs.projects)
        for project in projects:
            run_project_command(project, self.app.pargs.skip, 'branch', local=local, remote=remote)
