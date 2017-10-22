"""Configure clowder subparsers"""


def configure_argparse(parser, clowder, versions):
    """Configure clowder argparse"""
    subparsers = parser.add_subparsers(dest='clowder_command', metavar='SUBCOMMAND')
    _configure_subparsers(subparsers, clowder, versions)


def _configure_subparsers(subparsers, clowder, versions):
    """Configure clowder command subparsers"""
    _configure_subparser_branch(subparsers, clowder)
    _configure_subparser_clean(subparsers, clowder)
    _configure_subparser_diff(subparsers, clowder)
    _configure_subparser_forall(subparsers, clowder)
    _configure_subparser_herd(subparsers, clowder)
    _configure_subparser_init(subparsers)
    _configure_subparser_link(subparsers, versions)
    _configure_subparser_prune(subparsers, clowder)
    _configure_subparser_repo(subparsers)
    _configure_subparser_reset(subparsers, clowder)
    _configure_subparser_save(subparsers)
    _configure_subparser_start(subparsers, clowder)
    _configure_subparser_stash(subparsers, clowder)
    _configure_subparser_status(subparsers)
    _configure_subparser_sync(subparsers, clowder)
    _configure_subparser_version(subparsers)
    _configure_subparser_yaml(subparsers)


def _configure_subparser_branch(subparsers, clowder):
    """Configure clowder branch subparser and arguments"""
    branch_help = 'Display current branches'
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    parser_branch = subparsers.add_parser('branch', help=branch_help)
    branch_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_branch.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                               help=branch_help_skip)
    group_branch_options = parser_branch.add_mutually_exclusive_group()
    group_branch_options.add_argument('--all', '-a', action='store_true',
                                      help='show local and remote branches')
    group_branch_options.add_argument('--remote', '-r', action='store_true',
                                      help='show remote branches')
    group_branch = parser_branch.add_mutually_exclusive_group()
    branch_help_groups = _options_help_message(group_names, 'groups to show branches for')
    group_branch.add_argument('--groups', '-g', choices=group_names,
                              default=group_names, nargs='+', metavar='GROUP',
                              help=branch_help_groups)
    branch_help_projects = _options_help_message(project_names, 'projects to show branches for')
    group_branch.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                              help=branch_help_projects)


def _configure_subparser_clean(subparsers, clowder):
    """Configure clowder clean subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    clean_help = 'Discard current changes in projects'
    parser_clean = subparsers.add_parser('clean', help=clean_help)
    clean_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_clean.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                              help=clean_help_skip)
    parser_clean.add_argument('--all', '-a', action='store_true',
                              help='clean all the things')
    parser_clean.add_argument('--recursive', '-r', action='store_true',
                              help='clean submodules recursively')
    parser_clean.add_argument('-d', action='store_true',
                              help='remove untracked directories')
    parser_clean.add_argument('-f', action='store_true',
                              help='remove directories with .git subdirectory or file')
    parser_clean.add_argument('-X', action='store_true',
                              help='remove only files ignored by git')
    parser_clean.add_argument('-x', action='store_true',
                              help='remove all untracked files')
    group_clean = parser_clean.add_mutually_exclusive_group()
    clean_help_groups = _options_help_message(group_names, 'groups to clean')
    group_clean.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+', metavar='GROUP',
                             help=clean_help_groups)
    clean_help_projects = _options_help_message(project_names, 'projects to clean')
    group_clean.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=clean_help_projects)


def _configure_subparser_diff(subparsers, clowder):
    """Configure clowder diff subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    diff_help = 'Show git diff for projects'
    parser_diff = subparsers.add_parser('diff', help=diff_help)
    group_diff = parser_diff.add_mutually_exclusive_group()
    diff_help_groups = _options_help_message(group_names, 'groups to diff')
    group_diff.add_argument('--groups', '-g', choices=group_names,
                            default=group_names, nargs='+', metavar='GROUP',
                            help=diff_help_groups)
    diff_help_projects = _options_help_message(project_names, 'projects to diff')
    group_diff.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                            help=diff_help_projects)


def _configure_subparser_forall(subparsers, clowder):
    """Configure clowder forall subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    forall_help = 'Run command or script in project directories'
    parser_forall = subparsers.add_parser('forall', help=forall_help)
    forall_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_forall.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                               help=forall_help_skip)
    parser_forall.add_argument('--parallel', action='store_true',
                               help='run commands in parallel')
    parser_forall.add_argument('--ignore-errors', '-i', action='store_true',
                               help='ignore errors in command or script')
    group_forall_command = parser_forall.add_mutually_exclusive_group()
    group_forall_command.add_argument('--command', '-c', nargs=1, metavar='COMMAND',
                                      help='command or script to run in project directories')
    group_forall_targets = parser_forall.add_mutually_exclusive_group()
    forall_help_groups = _options_help_message(group_names, 'groups to run command or script for')
    group_forall_targets.add_argument('--groups', '-g', choices=group_names,
                                      default=group_names, nargs='+',
                                      metavar='GROUP', help=forall_help_groups,)
    forall_help_projects = _options_help_message(project_names, 'projects to run command or script for')
    group_forall_targets.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                                      help=forall_help_projects)


def _configure_subparser_herd(subparsers, clowder):
    """Configure clowder herd subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    herd_help = 'Clone and sync latest changes for projects'
    parser_herd = subparsers.add_parser('herd', help=herd_help)
    herd_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_herd.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                             help=herd_help_skip)
    parser_herd.add_argument('--parallel', action='store_true',
                             help='run commands in parallel')
    parser_herd.add_argument('--rebase', '-r', action='store_true',
                             help='use rebase instead of pull')
    parser_herd.add_argument('--depth', '-d', default=None, type=int, nargs=1, metavar='DEPTH',
                             help='depth to herd')
    group_herd = parser_herd.add_mutually_exclusive_group()
    group_herd.add_argument('--branch', '-b', nargs=1, default=None, metavar='BRANCH',
                            help='branch to herd if present')
    group_herd.add_argument('--tag', '-t', nargs=1, default=None, metavar='TAG',
                            help='tag to herd if present')
    group_herd = parser_herd.add_mutually_exclusive_group()
    herd_help_groups = _options_help_message(group_names, 'groups to herd')
    group_herd.add_argument('--groups', '-g', choices=group_names,
                            default=group_names, nargs='+', metavar='GROUP',
                            help=herd_help_groups)
    herd_help_projects = _options_help_message(project_names, 'projects to herd')
    group_herd.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                            help=herd_help_projects)


def _configure_subparser_init(subparsers):
    """Configure clowder init subparser and arguments"""
    init_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
    parser_init = subparsers.add_parser('init', help=init_help)
    parser_init.add_argument('url', metavar='URL', help='url of repo containing clowder.yaml')
    parser_init.add_argument('--branch', '-b', nargs=1, metavar='BRANCH',
                             help='branch of repo containing clowder.yaml')


def _configure_subparser_link(subparsers, versions):
    """Configure clowder link subparser and arguments"""
    parser_link = subparsers.add_parser('link', help='Symlink clowder.yaml version')
    link_help_version = _options_help_message(versions, 'version to symlink')
    parser_link.add_argument('--version', '-v', choices=versions, nargs=1, default=None, metavar='VERSION',
                             help=link_help_version)


def _configure_subparser_prune(subparsers, clowder):
    """Configure clowder prune subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    parser_prune = subparsers.add_parser('prune', help='Prune old branch')
    prune_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_prune.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                              help=prune_help_skip)
    parser_prune.add_argument('--force', '-f', action='store_true',
                              help='force prune branches')
    parser_prune.add_argument('branch', help='name of branch to remove', metavar='BRANCH')
    group_prune_options = parser_prune.add_mutually_exclusive_group()
    group_prune_options.add_argument('--all', '-a', action='store_true',
                                     help='prune local and remote branches')
    group_prune_options.add_argument('--remote', '-r', action='store_true',
                                     help='prune remote branches')
    group_prune = parser_prune.add_mutually_exclusive_group()
    prune_help_groups = _options_help_message(group_names, 'groups to prune branch for')
    group_prune.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+', metavar='GROUP',
                             help=prune_help_groups)
    prune_help_projects = _options_help_message(project_names, 'projects to prune branch for')
    group_prune.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=prune_help_projects)


def _configure_subparser_repo(subparsers):
    """Configure clowder repo subparser and arguments"""
    # clowder repo
    parser_repo = subparsers.add_parser('repo', help='Manage clowder repo')
    repo_subparsers = parser_repo.add_subparsers(dest='repo_command', metavar='SUBCOMMAND')
    # clowder repo add
    repo_add_help = 'Add files in clowder repo'
    parser_repo_add = repo_subparsers.add_parser('add', help=repo_add_help)
    parser_repo_add.add_argument('files', nargs='+', metavar='FILE',
                                 help='files to add')
    # clowder repo checkout
    repo_checkout_help = 'Checkout ref in clowder repo'
    parser_repo_checkout = repo_subparsers.add_parser('checkout', help=repo_checkout_help)
    parser_repo_checkout.add_argument('ref', nargs=1, metavar='REF',
                                      help='git ref to checkout')
    # clowder repo clean
    repo_clean_help = 'Discard changes in clowder repo'
    repo_subparsers.add_parser('clean', help=repo_clean_help)
    # clowder repo commit
    repo_commit_help = 'Commit current changes in clowder repo yaml files'
    parser_repo_commit = repo_subparsers.add_parser('commit', help=repo_commit_help)
    parser_repo_commit.add_argument('message', nargs=1, metavar='MESSAGE',
                                    help='commit message')
    # clowder repo run
    repo_run_help = 'Run command in clowder repo'
    parser_repo_run = repo_subparsers.add_parser('run', help=repo_run_help)
    repo_run_command_help = 'command to run in clowder repo directory'
    parser_repo_run.add_argument('command', nargs=1, metavar='COMMAND',
                                 help=repo_run_command_help)
    # clowder repo pull
    repo_pull_help = 'Pull upstream changes in clowder repo'
    repo_subparsers.add_parser('pull', help=repo_pull_help)
    # clowder repo push
    repo_subparsers.add_parser('push', help='Push changes in clowder repo')
    # clowder repo status
    repo_subparsers.add_parser('status', help='Print clowder repo git status')


def _configure_subparser_reset(subparsers, clowder):
    """Configure clowder reset subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    reset_help = 'Reset branches to upstream commits or check out detached HEADs for tags and shas'
    parser_reset = subparsers.add_parser('reset', help=reset_help)
    reset_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_reset.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                              help=reset_help_skip)
    parser_reset.add_argument('--parallel', action='store_true',
                              help='run commands in parallel')
    reset_help_timestamp = _options_help_message(project_names, 'project to reset timestamps relative to')
    parser_reset.add_argument('--timestamp', '-t', choices=project_names, default=None, nargs=1, metavar='TIMESTAMP',
                              help=reset_help_timestamp)
    group_reset = parser_reset.add_mutually_exclusive_group()
    reset_help_groups = _options_help_message(group_names, 'groups to reset')
    group_reset.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+', metavar='GROUP',
                             help=reset_help_groups)
    reset_help_projects = _options_help_message(project_names, 'projects to reset')
    group_reset.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=reset_help_projects)


def _configure_subparser_save(subparsers):
    """Configure clowder save subparser and arguments"""
    save_help = 'Create version of clowder.yaml for current repos'
    parser_save = subparsers.add_parser('save', help=save_help)
    parser_save.add_argument('version', help='version to save', metavar='VERSION')


def _configure_subparser_start(subparsers, clowder):
    """Configure clowder start subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    parser_start = subparsers.add_parser('start', help='Start a new feature')
    start_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_start.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                              help=start_help_skip)
    parser_start.add_argument('--tracking', '-t', action='store_true',
                              help='create remote tracking branch')
    parser_start.add_argument('branch', help='name of branch to create', metavar='BRANCH')
    group_start = parser_start.add_mutually_exclusive_group()
    start_help_groups = _options_help_message(group_names, 'groups to start feature branch for')
    group_start.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+', metavar='GROUP',
                             help=start_help_groups)
    start_help_projects = _options_help_message(project_names, 'projects to start feature branch for')
    group_start.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=start_help_projects)


def _configure_subparser_stash(subparsers, clowder):
    """Configure clowder stash subparser and arguments"""
    group_names = _group_names(clowder)
    project_names = _project_names(clowder)
    parser_stash = subparsers.add_parser('stash', help='Stash current changes')
    stash_help_skip = _options_help_message(project_names, 'projects to skip')
    parser_stash.add_argument('--skip', '-s', choices=project_names, nargs='+', metavar='PROJECT',
                              help=stash_help_skip)
    group_stash = parser_stash.add_mutually_exclusive_group()
    stash_help_groups = _options_help_message(group_names, 'groups to stash')
    group_stash.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+', metavar='GROUP',
                             help=stash_help_groups)
    stash_help_projects = _options_help_message(project_names, 'projects to stash')
    group_stash.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=stash_help_projects)


def _configure_subparser_status(subparsers):
    """Configure clowder status subparser and arguments"""
    parser_status = subparsers.add_parser('status', help='Print project status')
    parser_status.add_argument('--fetch', '-f', action='store_true',
                               help='fetch projects before printing status')


def _configure_subparser_sync(subparsers, clowder):
    """Configure clowder sync subparser and arguments"""
    project_names = _fork_project_names(clowder)
    parser_sync = subparsers.add_parser('sync', help='Sync fork with upstream remote')
    parser_sync.add_argument('--parallel', action='store_true',
                             help='run commands in parallel')
    parser_sync.add_argument('--rebase', '-r', action='store_true',
                             help='use rebase instead of pull')
    sync_help_projects = _options_help_message(project_names, 'projects to sync')
    parser_sync.add_argument('--projects', '-p', choices=project_names, nargs='+', metavar='PROJECT',
                             help=sync_help_projects)


def _configure_subparser_version(subparsers):
    """Configure clowder version subparser and arguments"""
    subparsers.add_parser('version', help='Print clowder version')


def _configure_subparser_yaml(subparsers):
    """Configure clowder yaml subparser and arguments"""
    parser_yaml = subparsers.add_parser('yaml', help='Print clowder.yaml information')
    parser_yaml.add_argument('--resolved', '-r', action='store_true',
                             help='print resolved clowder.yaml')


def _fork_project_names(clowder):
    """Return group options"""
    if clowder:
        return clowder.get_all_fork_project_names()
    return ''


def _group_names(clowder):
    """Return group options"""
    if clowder:
        return clowder.get_all_group_names()
    return ''


def _options_help_message(options, message):
    """Help message for groups option"""
    if options == '' or options is None:
        return message
    help_message = '''
                   {0}:
                   {1}
                   '''
    return help_message.format(message, ', '.join(options))


def _project_names(clowder):
    """Return project options"""
    if clowder:
        return clowder.get_all_project_names()
    return ''
