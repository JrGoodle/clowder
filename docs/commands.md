# `clowder` Commands

Examples based on the [Swift projects clowder.yml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yml)

## Table of Contents

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
  * [clowder version](#clowder-version)
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

# Only herd projects in swift and llvm groups
clowder herd swift llvm

# Only herd swift project
clowder herd apple/swift
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

# Run command for projects in llvm group
clowder forall -c "git status" -g llvm

# Run script for projects in llvm group
clowder forall -c "/path/to/script.sh" -g llvm

# Run command for swift project
clowder forall apple/swift -c "git status"

# Run script for swift project
clowder forall apple/swift -c "/path/to/script.sh"
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

# Print local branches in llvm group
clowder branch llvm

# Print local branches in swift project
clowder branch apple/swift
```

### clowder checkout

```bash
# Checkout branches
clowder checkout branch_name

# Checkout branches in llvm group
clowder checkout branch_name llvm

# Checkout branches in swift project
clowder checkout branch_name apple/swift
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

# Discard changes in projects in llvm group
clowder clean llvm

# Discard changes in swift project
clowder clean apple/swift

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

# Print git diff status for projects in llvm group
clowder diff llvm

# Print git diff status for swift project
clowder diff apple/swift
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

# Prune branch 'stale_branch' for projects in llvm group
clowder prune stale_branch llvm

# Prune branch 'stale_branch' in swift project
clowder prune stale_branch apple/swift
```

### clowder reset

Reset branches to upstream state

```bash
# Reset branches in all projects
clowder reset

# Reset branches in all projects to closest timestamp to swift project
clowder reset --timestamp apple/swift

# Reset branches in projects in llvm group
clowder reset llvm

# Reset branches in swift project
clowder reset apple/swift
```

### clowder start

Start a new feature branch or check out if it already exists

```bash
# Create new local branch 'my_feature' for all projects
clowder start my_feature

# Create new local and remote tracking branch 'my_feature' for all projects
clowder start -t my_feature

# Create new local branch 'my_feature' for projects in llvm group
clowder start my_feature llvm

# Create new local branch 'my_feature' in swift project
clowder start my_feature apple/swift
```

### clowder stash

Stash changes in dirty repositories

```bash
# Stash changes in all projects
clowder stash

# Stash changes in projects in llvm group
clowder stash llvm

# Stash changes in swift project
clowder stash apple/swift
```

## clowder repo commands

### clowder link

Set `clowder.yml` symlink

```bash
# Point clowder.yml symlink to default clowder.yml file
clowder link

# Point clowder.yml symlink to saved version
clowder link 0.1
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
# Save a version of clowder.yml with current commit sha's
clowder save 0.1
```

## other commands

### clowder version

Print version of `clowder` command line tool

```bash
clowder --version
```

### clowder yaml

Print information about clowder.yml files

```bash
# Print clowder.yml file(s) referenced from current symlink and imports
clowder yaml

# Print resolved clowder.yml
clowder yaml -r
```
