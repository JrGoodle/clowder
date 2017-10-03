"""Configure clowder subparsers"""

def configure_argparse(parser, clowder, versions):
    """Configure clowder argparse"""
    parser.add_argument('--version', '-v', action='store_true',
                        dest='clowder_version', help='print clowder version')
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
    _configure_subparser_save(subparsers)
    _configure_subparser_start(subparsers, clowder)
    _configure_subparser_stash(subparsers, clowder)
    _configure_subparser_status(subparsers)
    _configure_subparser_sync(subparsers, clowder)
    _configure_subparser_yaml(subparsers)

def _configure_subparser_branch(subparsers, clowder):
    """Configure clowder branch subparser and arguments"""
    branch_help = 'Display current branches'
    parser_branch = subparsers.add_parser('branch', help=branch_help)
    group_branch_options = parser_branch.add_mutually_exclusive_group()
    group_branch_options.add_argument('--all', '-a', action='store_true',
                                      help='show local and remote branches')
    group_branch_options.add_argument('--remote', '-r', action='store_true',
                                      help='show remote branches')
    group_branch = parser_branch.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        branch_help_groups = 'groups to show branches for'
    else:
        branch_help_groups = '''
                             groups to show branches for:
                             {0}
                             '''
        branch_help_groups = branch_help_groups.format(', '.join(group_names))
    group_branch.add_argument('--groups', '-g', choices=group_names,
                              default=group_names, nargs='+',
                              help=branch_help_groups, metavar='GROUP')
    if project_names is '':
        branch_help_projects = 'projects to show branches for'
    else:
        branch_help_projects = '''
                               projects to show branches for:
                               {0}
                               '''
        branch_help_projects = branch_help_projects.format(', '.join(project_names))
    group_branch.add_argument('--projects', '-p', choices=project_names,
                              nargs='+', help=branch_help_projects, metavar='PROJECT')

def _configure_subparser_clean(subparsers, clowder):
    """Configure clowder clean subparser and arguments"""
    clean_help = 'Discard current changes in projects'
    parser_clean = subparsers.add_parser('clean', help=clean_help)
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
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        clean_help_groups = 'groups to clean'
    else:
        clean_help_groups = '''
                             groups to clean:
                             {0}
                             '''
        clean_help_groups = clean_help_groups.format(', '.join(group_names))
    group_clean.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+',
                             help=clean_help_groups, metavar='GROUP')
    if project_names is '':
        clean_help_projects = 'projects to clean'
    else:
        clean_help_projects = '''
                               projects to clean:
                               {0}
                               '''
        clean_help_projects = clean_help_projects.format(', '.join(project_names))
    group_clean.add_argument('--projects', '-p', choices=project_names,
                             nargs='+', help=clean_help_projects, metavar='PROJECT')

def _configure_subparser_diff(subparsers, clowder):
    """Configure clowder diff subparser and arguments"""
    diff_help = 'Show git diff for projects'
    parser_diff = subparsers.add_parser('diff', help=diff_help)
    group_diff = parser_diff.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        diff_help_groups = 'groups to diff'
    else:
        diff_help_groups = '''
                           groups to diff:
                           {0}
                           '''
        diff_help_groups = diff_help_groups.format(', '.join(group_names))
    group_diff.add_argument('--groups', '-g', choices=group_names,
                            default=group_names, nargs='+',
                            help=diff_help_groups, metavar='GROUP')
    if project_names is '':
        diff_help_projects = 'projects to diff'
    else:
        diff_help_projects = '''
                             projects to diff:
                             {0}
                             '''
        diff_help_projects = diff_help_projects.format(', '.join(project_names))
    group_diff.add_argument('--projects', '-p', choices=project_names,
                            nargs='+', help=diff_help_projects, metavar='PROJECT')

def _configure_subparser_forall(subparsers, clowder):
    """Configure clowder forall subparser and arguments"""
    forall_help = 'Run command or script in project directories'
    parser_forall = subparsers.add_parser('forall', help=forall_help)
    parser_forall.add_argument('--ignore-errors', '-i', action='store_true',
                               help='ignore errors in command or script')
    group_forall_command = parser_forall.add_mutually_exclusive_group()
    group_forall_command.add_argument('--command', '-c', nargs=1, metavar='COMMAND',
                                      help='command or script to run in project directories')
    group_forall_targets = parser_forall.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        forall_help_groups = 'groups to run command or script for'
    else:
        forall_help_groups = '''
                             groups to run command or script for:
                             {0}
                             '''
        forall_help_groups = forall_help_groups.format(', '.join(group_names))
    group_forall_targets.add_argument('--groups', '-g', choices=group_names,
                                      default=group_names, nargs='+',
                                      help=forall_help_groups, metavar='GROUP')
    if project_names is '':
        forall_help_projects = 'projects to run command or script for'
    else:
        forall_help_projects = '''
                               projects to run command or script for:
                               {0}
                               '''
        forall_help_projects = forall_help_projects.format(', '.join(project_names))
    group_forall_targets.add_argument('--projects', '-p', choices=project_names,
                                      nargs='+', help=forall_help_projects,
                                      metavar='PROJECT')

def _configure_subparser_herd(subparsers, clowder):
    """Configure clowder herd subparser and arguments"""
    herd_help = 'Clone and sync latest changes for projects'
    parser_herd = subparsers.add_parser('herd', help=herd_help)
    parser_herd.add_argument('--depth', '-d', default=None, type=int, nargs=1,
                             help='depth to herd', metavar='DEPTH')
    parser_herd.add_argument('--branch', '-b', nargs=1, default=None,
                             help='branch to herd if present', metavar='BRANCH')
    group_herd = parser_herd.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        herd_help_groups = 'groups to herd'
    else:
        herd_help_groups = '''
                             groups to herd:
                             {0}
                             '''
        herd_help_groups = herd_help_groups.format(', '.join(group_names))
    group_herd.add_argument('--groups', '-g', choices=group_names,
                            default=group_names, nargs='+',
                            help=herd_help_groups, metavar='GROUP')
    if project_names is '':
        herd_help_projects = 'projects to herd'
    else:
        herd_help_projects = '''
                               projects to herd:
                               {0}
                               '''
        herd_help_projects = herd_help_projects.format(', '.join(project_names))
    group_herd.add_argument('--projects', '-p', choices=project_names,
                            nargs='+', help=herd_help_projects, metavar='PROJECT')

def _configure_subparser_init(subparsers):
    """Configure clowder init subparser and arguments"""
    init_help = 'Clone repository to clowder directory and create clowder.yaml symlink'
    parser_init = subparsers.add_parser('init', help=init_help)
    parser_init.add_argument('url', help='url of repo containing clowder.yaml', metavar='URL')
    parser_init.add_argument('--branch', '-b', nargs=1,
                             help='branch of repo containing clowder.yaml', metavar='BRANCH')

def _configure_subparser_link(subparsers, versions):
    """Configure clowder link subparser and arguments"""
    parser_link = subparsers.add_parser('link', help='Symlink clowder.yaml version')
    if versions is None:
        link_help_version = 'version to symlink'
    else:
        link_help_version = '''
                               version to symlink:
                               {0}
                               '''
        link_help_version = link_help_version.format(', '.join(versions))
    parser_link.add_argument('--version', '-v', choices=versions, nargs=1,
                             default=None, help=link_help_version, metavar='VERSION')

def _configure_subparser_prune(subparsers, clowder):
    """Configure clowder prune subparser and arguments"""
    parser_prune = subparsers.add_parser('prune', help='Prune old branch')
    parser_prune.add_argument('--force', '-f', action='store_true',
                              help='force prune branches')
    parser_prune.add_argument('branch', help='name of branch to remove', metavar='BRANCH')
    group_prune_options = parser_prune.add_mutually_exclusive_group()
    group_prune_options.add_argument('--all', '-a', action='store_true',
                                     help='prune local and remote branches')
    group_prune_options.add_argument('--remote', '-r', action='store_true',
                                     help='prune remote branches')
    group_prune = parser_prune.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        prune_help_groups = 'groups to prune branch for'
    else:
        prune_help_groups = '''
                             groups to prune branch for:
                             {0}
                             '''
        prune_help_groups = prune_help_groups.format(', '.join(group_names))
    group_prune.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+',
                             help=prune_help_groups, metavar='GROUP')
    if project_names is '':
        prune_help_projects = 'projects to prune branch for'
    else:
        prune_help_projects = '''
                               projects to prune branch for:
                               {0}
                               '''
        prune_help_projects = prune_help_projects.format(', '.join(project_names))
    group_prune.add_argument('--projects', '-p', choices=project_names,
                             nargs='+', help=prune_help_projects, metavar='PROJECT')

def _configure_subparser_repo(subparsers):
    """Configure clowder repo subparser and arguments"""
    # clowder repo
    parser_repo = subparsers.add_parser('repo', help='Manage clowder repo')
    repo_subparsers = parser_repo.add_subparsers(dest='repo_command', metavar='SUBCOMMAND')
    # clowder repo add
    repo_add_help = 'Add files in clowder repo'
    parser_repo_add = repo_subparsers.add_parser('add', help=repo_add_help)
    parser_repo_add.add_argument('files', nargs='+',
                                 help='files to add', metavar='FILE')
    # clowder repo checkout
    repo_checkout_help = 'Checkout ref in clowder repo'
    parser_repo_checkout = repo_subparsers.add_parser('checkout', help=repo_checkout_help)
    parser_repo_checkout.add_argument('ref', nargs=1,
                                      help='git ref to checkout', metavar='REF')
    # clowder repo clean
    repo_clean_help = 'Discard changes in clowder repo'
    repo_subparsers.add_parser('clean', help=repo_clean_help)
    # clowder repo commit
    repo_commit_help = 'Commit current changes in clowder repo yaml files'
    parser_repo_commit = repo_subparsers.add_parser('commit', help=repo_commit_help)
    parser_repo_commit.add_argument('message', nargs=1,
                                    help='commit message', metavar='MESSAGE')
    # clowder repo run
    repo_run_help = 'Run command in clowder repo'
    parser_repo_run = repo_subparsers.add_parser('run', help=repo_run_help)
    repo_run_command_help = 'command to run in clowder repo directory'
    parser_repo_run.add_argument('command', nargs=1,
                                 help=repo_run_command_help, metavar='COMMAND')
    # clowder repo pull
    repo_pull_help = 'Pull upstream changes in clowder repo'
    repo_subparsers.add_parser('pull', help=repo_pull_help)
    # clowder repo push
    repo_subparsers.add_parser('push', help='Push changes in clowder repo')
    # clowder repo status
    repo_subparsers.add_parser('status', help='Print clowder repo git status')

def _configure_subparser_save(subparsers):
    """Configure clowder save subparser and arguments"""
    save_help = 'Create version of clowder.yaml for current repos'
    parser_save = subparsers.add_parser('save', help=save_help)
    parser_save.add_argument('version', help='version to save', metavar='VERSION')

def _configure_subparser_start(subparsers, clowder):
    """Configure clowder start subparser and arguments"""
    parser_start = subparsers.add_parser('start', help='Start a new feature')
    parser_start.add_argument('--tracking', '-t', action='store_true',
                              help='create remote tracking branch')
    parser_start.add_argument('branch', help='name of branch to create', metavar='BRANCH')
    group_start = parser_start.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        start_help_groups = 'groups to start feature branch for'
    else:
        start_help_groups = '''
                             groups to start feature branch for:
                             {0}
                             '''
        start_help_groups = start_help_groups.format(', '.join(group_names))
    group_start.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+',
                             help=start_help_groups, metavar='GROUP')
    if project_names is '':
        start_help_projects = 'projects to start feature branch for'
    else:
        start_help_projects = '''
                               projects to start feature branch for:
                               {0}
                               '''
        start_help_projects = start_help_projects.format(', '.join(project_names))
    group_start.add_argument('--projects', '-p', choices=project_names,
                             nargs='+', help=start_help_projects, metavar='PROJECT')

def _configure_subparser_stash(subparsers, clowder):
    """Configure clowder stash subparser and arguments"""
    parser_stash = subparsers.add_parser('stash',
                                         help='Stash current changes')
    group_stash = parser_stash.add_mutually_exclusive_group()
    if clowder is None:
        group_names = ''
        project_names = ''
    else:
        group_names = clowder.get_all_group_names()
        project_names = clowder.get_all_project_names()
    if group_names is '':
        stash_help_groups = 'groups to stash'
    else:
        stash_help_groups = '''
                             groups to stash:
                             {0}
                             '''
        stash_help_groups = stash_help_groups.format(', '.join(group_names))
    group_stash.add_argument('--groups', '-g', choices=group_names,
                             default=group_names, nargs='+',
                             help=stash_help_groups, metavar='GROUP')
    if project_names is '':
        stash_help_projects = 'projects to stash'
    else:
        stash_help_projects = '''
                               projects to stash:
                               {0}
                               '''
        stash_help_projects = stash_help_projects.format(', '.join(project_names))
    group_stash.add_argument('--projects', '-p', choices=project_names,
                             nargs='+', help=stash_help_projects, metavar='PROJECT')

def _configure_subparser_status(subparsers):
    """Configure clowder status subparser and arguments"""
    parser_status = subparsers.add_parser('status', help='Print project status')
    parser_status.add_argument('--fetch', '-f', action='store_true',
                               help='fetch projects before printing status')

def _configure_subparser_sync(subparsers, clowder):
    """Configure clowder sync subparser and arguments"""
    if clowder is None:
        project_names = ''
    else:
        project_names = clowder.get_all_fork_project_names()
    parser_sync = subparsers.add_parser('sync', help='Sync fork with upstream remote')
    if project_names is '':
        sync_help_projects = 'projects to sync'
    else:
        sync_help_projects = '''
                               projects to sync:
                               {0}
                               '''
        sync_help_projects = sync_help_projects.format(', '.join(project_names))
    parser_sync.add_argument('--projects', '-p', choices=project_names,
                             nargs='+', help=sync_help_projects, metavar='PROJECT')

def _configure_subparser_yaml(subparsers):
    """Configure clowder yaml subparser and arguments"""
    parser_yaml = subparsers.add_parser('yaml', help='Print clowder.yaml information')
    parser_yaml.add_argument('--resolved', '-r', action='store_true',
                             help='print resolved clowder.yaml')
