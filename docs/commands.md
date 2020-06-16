# `clowder` Commands

Examples based on the [Swift projects clowder.yml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yml)

* [main commands](#main-commands)
  * [clowder init](#clowder-init)
  * [clowder herd](#clowder-herd)
  * [clowder status](#clowder-status)
  * [clowder forall](#clowder-forall)
* [git commands](#git-commands)
  * [clowder branch](#clowder-branch)
  * [clowder checkout](#clowder-checkout)
  * [clowder clean](#clowder-clean)
  * [clowder diff](#clowder-diff)
  * [clowder prune](#clowder-prune)
  * [clowder reset](#clowder-reset)
  * [clowder start](#clowder-start)
  * [clowder stash](#clowder-stash)
* [clowder repo commands](#clowder-repo-commands)
  * [clowder link](#clowder-link)
  * [clowder repo](#clowder-repo)
  * [clowder save](#clowder-save)
* [other commands](#other-commands)
  * [clowder config](#clowder-config-EXPERIMENTAL)
    * [clowder config get](#clowder-config-get-EXPERIMENTAL)
    * [clowder config set](#clowder-config-set-EXPERIMENTAL)
    * [clowder config clear](#clowder-config-clear-EXPERIMENTAL)
  * [clowder yaml](#clowder-yaml)

## main commands

### clowder init

Clone repo containing `clowder.yml` file (referred to as the "clowder repo")

```bash
# Clone clowder repo
clowder init https://github.com/jrgoodle/swift-clowder.git

# Clone clowder repo from branch 'tags'
clowder init https://github.com/jrgoodle/cats.git -b tags
```

### clowder herd

Update with latest changes

```bash
# Herd a shallow clone to specified depth
clowder herd -d 1

# Herd using rebase instead of pull
clowder herd -r

# Herd a specified branch if it exists, otherwise use default ref
clowder herd -b my_branch

# Herd a specified tag if it exists, otherwise use default ref
clowder herd -t my_tag

# Herd all projects
clowder herd all linux

# Only herd swift project
clowder herd swift
```

### clowder status

Print status of projects

```bash
# Print status of projects
clowder status

# Fetch upstream changes for projects before printing status
clowder status -f
```

### clowder forall

Runs command or script in project directories

```bash
# Run command in all project directories
clowder forall -c "git status"

# Run script in all project directories
clowder forall -c "/path/to/script.sh"

# Run command in all project directories, ignoring errors
clowder forall -ic "git status"

# Run script in all project directories, ignoring errors
clowder forall -ic "/path/to/script.sh"

# Run command for all projects
clowder forall all linux -c "git status"

# Run script for all projects
clowder forall all linux -c "/path/to/script.sh"

# Run command for swift project
clowder forall swift -c "git status"

# Run script for swift project
clowder forall swift -c "/path/to/script.sh"
```

The following environment variables are available for use in commands and scripts:

* `CLOWDER_PATH` is the absolute path to the root directory the clowder repo was initialized in
* `PROJECT_PATH` is the absolute path to the project directory
* `PROJECT_NAME` is the unique name of the project
* `PROJECT_REMOTE` is the name of the project's remote
* `PROJECT_REF` is the project ref as written in the `clowder.yml` file

If a fork is specified, the following environment variables are also available for use in commands and scripts:

* `FORK_REMOTE` is the name of the fork's remote
* `FORK_NAME` is the unique name of the fork
* `FORK_REF` is the project ref as written in the `clowder.yml` file

## git commands

### clowder branch

```bash
# Print all local branches
clowder branch

# Print all remote branches
clowder branch -r

# Print all local and remote branches
clowder branch -a

# Print local branches in llvm project
clowder branch swift

# Print local branches in all projects
clowder branch all linux
```

### clowder checkout

```bash
# Checkout branches
clowder checkout branch_name

# Checkout branches in all projects
clowder checkout branch_name all linux

# Checkout branches in swift project
clowder checkout branch_name swift
```

### clowder clean

Discards changes in dirty repositories

```bash
# Discard changes in all projects
# Equivalent to:
# git clean -f; git reset --hard; git rebase --abort
clowder clean

# Clean all the things
# Equivalent to:
# git clean -ffdx; git reset --hard; git rebase --abort
# git submodule foreach --recursive git clean -ffdx
# git submodule foreach --recursive git reset --hard
# git submodule update --checkout --recursive --force
clowder clean -a

# Discard changes in all projects
clowder clean all linux

# Discard changes in swift project
clowder clean swift

# Remove untracked directories in addition to untracked files
# Equivalent to:
# git clean -fd; git reset --hard; git rebase --abort
clowder clean -d

# Delete directories with .git sub directory or file
# Equivalent to:
# git clean -ff; git reset --hard; git rebase --abort
clowder clean -f

# Remove only files ignored by git
# Equivalent to:
# git clean -fX; git reset --hard; git rebase --abort
clowder clean -X

# Remove all untracked files
# Equivalent to:
# git clean -fx; git reset --hard; git rebase --abort
clowder clean -x

# Recursively clean submodules
# Equivalent to:
# git clean -f; git reset --hard; git rebase --abort
# git submodule foreach --recursive git clean -ffdx
# git submodule foreach --recursive git reset --hard
# git submodule update --checkout --recursive --force
clowder clean -r
```

### clowder diff

Equivalent to running `git status -vv` in project directories

```bash
# Print git diff status for all projects
clowder diff

# Print git diff status for all projects
clowder diff all linux

# Print git diff status for swift project
clowder diff swift
```

### clowder prune

Prune local or remote branches

```bash
# Prune branch 'stale_branch' for all projects
clowder prune stale_branch

# Force prune branch 'stale_branch' for all projects
clowder prune -f stale_branch

# Prune remote branch 'stale_branch' for all projects
clowder prune -r stale_branch

# Prune local and remote branch 'stale_branch' for all projects
clowder prune -a stale_branch

# Force prune local and remote branch 'stale_branch' for all projects
clowder prune -af stale_branch

# Prune branch 'stale_branch' for all projects
clowder prune stale_branch all linux

# Prune branch 'stale_branch' in swift project
clowder prune stale_branch swift
```

### clowder reset

Reset branches to upstream state

```bash
# Reset branches in all projects
clowder reset

# Reset branches in all projects to closest timestamp to swift project
clowder reset --timestamp swift

# Reset branches in all projects
clowder reset all linux

# Reset branches in swift project
clowder reset swift
```

### clowder start

Start a new feature branch or check out if it already exists

```bash
# Create new local branch 'my_feature' for all projects
clowder start my_feature

# Create new local and remote tracking branch 'my_feature' for all projects
clowder start -t my_feature

# Create new local branch 'my_feature' for all projects
clowder start my_feature all linux

# Create new local branch 'my_feature' in swift project
clowder start my_feature swift
```

### clowder stash

Stash changes in dirty repositories

```bash
# Stash changes in all projects
clowder stash

# Stash changes in all projects
clowder stash all linux

# Stash changes in swift project
clowder stash swift
```

## clowder repo commands

### clowder link

Set `clowder.yml` symlink

```bash
# Point clowder.yml symlink to default clowder.yml file
clowder link

# Point clowder.yml symlink to saved version
clowder link swift-5.0-branch
```

### clowder repo

Convenience commands for managing clowder repo (the `.clowder` directory)

More advanced needs may require changing to the `.clowder` directory and running commands directly

```bash
# Add modified files in working tree to the index
clowder repo add .

# Checkout git ref in clowder repo
clowder repo checkout my_branch

# Discard current changes in clowder repo
clowder repo clean

# Commit changes to yaml files in clowder repo
clowder repo commit 'commit message'

# Pull latest changes in clowder repo
clowder repo pull

# Push latest changes in clowder repo
clowder repo push

# Run command in .clowder directory
clowder repo run 'git status'

# Print clowder repo git status
clowder repo status
```

### clowder save

Save a `clowder.yml` version with the information from currently checked out repositories

Versions are saved to `.clowder/<version_name>.clowder.yml`

```bash
# Save swift-42.0.clowder.yml version with current commit sha's
clowder save swift-42.0
```

## other commands

### clowder config **_EXPERIMENTAL_**

#### clowder config get **_EXPERIMENTAL_**

```bash
# Print all set config values
clowder config get
```

#### clowder config set **_EXPERIMENTAL_**

```bash
# Set config values
clowder config set rebase
clowder config set jobs
clowder config set projects swift
clowder config set protocol ssh
```

#### clowder config clear **_EXPERIMENTAL_**

```bash
# Clear config values
clowder config clear rebase
clowder config clear jobs
clowder config clear projects
clowder config clear protocol
```

### clowder yaml

Print information about clowder.yml files

```bash
# Print current clowder.yml file
clowder yaml

# Print resolved clowder.yml with current commit sha's
clowder yaml -r
```
