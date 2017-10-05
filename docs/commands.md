# `clowder` Commands

- [clowder branch](#clowder-branch)
- [clowder clean](#clowder-clean)
- [clowder diff](#clowder-diff)
- [clowder forall](#clowder-forall)
- [clowder herd](#clowder-herd)
- [clowder init](#clowder-init)
- [clowder link](#clowder-link)
- [clowder prune](#clowder-prune)
- [clowder repo](#clowder-repo)
- [clowder save](#clowder-save)
- [clowder start](#clowder-start)
- [clowder stash](#clowder-stash)
- [clowder status](#clowder-status)
- [clowder sync](#clowder-sync)
- [clowder yaml](#clowder-yaml)

Examples based on the [Swift projects clowder.yaml](https://github.com/JrGoodle/swift-clowder/blob/master/clowder.yaml)

---

```bash
# Print all local branches
$ clowder branch

# Print all remote branches
$ clowder branch -r

# Print all local and remote branches
$ clowder branch -a

# Print local branches in llvm group
$ clowder branch -g llvm

# Print local branches in swift project
$ clowder branch -p apple/swift
```

---

## `clowder clean`

Discards changes in dirty repositories

```bash
# Discard changes in all projects
# Equivalent to:
# git clean -f; git reset --hard; git rebase --abort
$ clowder clean

# Clean all the things
# Equivalent to:
# git clean -ffdx; git reset --hard; git rebase --abort
# git submodule foreach --recursive git clean -ffdx
# git submodule foreach --recursive git reset --hard
# git submodule update --checkout --recursive --force
$ clowder clean -a

# Discard changes in projects in llvm group
$ clowder clean -g llvm

# Discard changes in swift project
$ clowder clean -p apple/swift

# Remove untracked directories in addition to untracked files
# Equivalent to:
# git clean -fd; git reset --hard; git rebase --abort
$ clowder clean -d

# Delete directories with .git sub directory or file
# Equivalent to:
# git clean -ff; git reset --hard; git rebase --abort
$ clowder clean -f

# Remove only files ignored by git
# Equivalent to:
# git clean -fX; git reset --hard; git rebase --abort
$ clowder clean -X

# Remove all untracked files
# Equivalent to:
# git clean -fx; git reset --hard; git rebase --abort
$ clowder clean -x

# Recursively clean submodules
# Equivalent to:
# git clean -f; git reset --hard; git rebase --abort
# git submodule foreach --recursive git clean -ffdx
# git submodule foreach --recursive git reset --hard
# git submodule update --checkout --recursive --force
$ clowder clean -r
```

---

## `clowder diff`

Equivalent to running `git status -vv` in project directories

```bash
# Print git diff status for all projects
$ clowder diff

# Print git diff status for projects in llvm group
$ clowder diff -g llvm

# Print git diff status for swift project
$ clowder diff -p apple/swift
```

---

## `clowder forall`

Runs command or script in project directories

```bash
# Run command in all project directories
$ clowder forall -c "git status"

# Run script in all project directories
$ clowder forall -c "/path/to/script.sh"

# Run command in all project directories, ignoring errors
$ clowder forall -ic "git status"

# Run script in all project directories, ignoring errors
$ clowder forall -ic "/path/to/script.sh"

# Run command for projects in llvm group
$ clowder forall -c "git status" -g llvm

# Run script for projects in llvm group
$ clowder forall -c "/path/to/script.sh" -g llvm

# Run command for swift project
$ clowder forall -c "git status" -p apple/swift

# Run script for swift project
$ clowder forall -c "/path/to/script.sh" -p apple/swift
```

The following environment variables are available for use in commands and scripts:

- `CLOWDER_PATH` is the absolute path to the root directory the clowder repo was initialized in
- `PROJECT_PATH` is the absolute path to the project directory
- `PROJECT_NAME` is the unique name of the project
- `PROJECT_REMOTE` is the name of the project's remote
- `PROJECT_REF` is the project ref as written in the `clowder.yaml` file

---

## `clowder herd`

Update with latest changes

```bash
# Herd a shallow clone to specified depth
$ clowder herd -d 1

# Herd a specified branch if it exists, otherwise use default ref
$ clowder herd -b my_branch

# Only herd projects in swift and llvm groups
$ clowder herd -g swift llvm

# Only herd swift project
$ clowder herd -p apple/swift
```

---

## `clowder init`

Clone repo containing `clowder.yaml` file (referred to as the "clowder repo")

```bash
# Clone clowder repo
$ clowder init https://github.com/jrgoodle/swift-clowder.git

# Clone clowder repo from branch 'tags'
$ clowder init https://github.com/jrgoodle/cats.git -b tags
```

---

## `clowder link`

Set `clowder.yaml` symlink

```bash
# Point clowder.yaml symlink to default clowder.yaml file
$ clowder link

# Point clowder.yaml symlink to saved version
$ clowder link -v 0.1
```

---

## `clowder prune`

Prune local or remote branches

```bash
# Prune branch 'stale_branch' for all projects
$ clowder prune stale_branch

# Force prune branch 'stale_branch' for all projects
$ clowder prune -f stale_branch

# Prune remote branch 'stale_branch' for all projects
$ clowder prune -r stale_branch

# Prune local and remote branch 'stale_branch' for all projects
$ clowder prune -a stale_branch

# Force prune local and remote branch 'stale_branch' for all projects
$ clowder prune -af stale_branch

# Prune branch 'stale_branch' for projects in llvm group
$ clowder prune stale_branch -g llvm

# Prune branch 'stale_branch' in swift project
$ clowder prune stale_branch -p apple/swift
```

---

## `clowder repo`

Convenience commands for managing clowder repo (the `.clowder` directory)

More advanced needs may require changing to the `.clowder` directory and running commands directly

```bash
# Add modified files in working tree to the index
$ clowder repo add .

# Checkout git ref in clowder repo
$ clowder repo checkout my_branch

# Discard current changes in clowder repo
$ clowder repo clean

# Commit changes to yaml files in clowder repo
$ clowder repo commit 'commit message'

# Pull latest changes in clowder repo
$ clowder repo pull

# Push latest changes in clowder repo
$ clowder repo push

# Run command in .clowder directory
$ clowder repo run 'git status'

# Print clowder repo git status
$ clowder repo status
```

---

## `clowder save`

Save a `clowder.yaml` version with the information from currently checked out repositories

Versions are saved to `.clowder/versions/<version_name>/clowder.yaml`

```bash
# Save a version of clowder.yaml with current commit sha's
$ clowder save 0.1
```

---

## `clowder start`

Start a new feature branch or check out if it already exists

```bash
# Create new local branch 'my_feature' for all projects
$ clowder start my_feature

# Create new local and remote tracking branch 'my_feature' for all projects
$ clowder start -t my_feature

# Create new local branch 'my_feature' for projects in llvm group
$ clowder start my_feature -g llvm

# Create new local branch 'my_feature' in swift project
$ clowder start my_feature -p apple/swift
```

---

## `clowder stash`

Stash changes in dirty repositories

```bash
# Stash changes in all projects
$ clowder stash

# Stash changes in projects in llvm group
$ clowder stash -g llvm

# Stash changes in swift project
$ clowder stash -p apple/swift
```

---

## `clowder status`

Print status of projects

```bash
# Print status of projects
$ clowder status

# Fetch upstream changes for projects before printing status
$ clowder status -f
```

---

## `clowder sync`

Sync default fork branches with upstream remotes

```bash
# Sync all forks with upstream remotes
$ clowder sync

# Sync swift fork with upstream remote
$ clowder sync -p apple/swift
```

---

## `clowder yaml`

Print information about clowder.yaml files

```bash
# Print clowder.yaml file(s) referenced from current symlink and imports
$ clowder yaml

# Print resolved clowder.yaml
$ clowder yaml -r
```
