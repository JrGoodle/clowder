# `clowder` Commands

- [clowder clean](#clowder-clean)
- [clowder diff](#clowder-diff)
- [clowder forall](#clowder-forall)
- [clowder herd](#clowder-herd)
- [clowder init](#clowder-init)
- [clowder link](#clowder-link)
- [clowder repo](#clowder-repo)
- [clowder save](#clowder-save)
- [clowder start](#clowder-start)
- [clowder stash](#clowder-stash)
- [clowder status](#clowder-status)
- [clowder prune](#clowder-prune)

---

## `clowder clean`

Discards changes in dirty repositories

```bash
# Discard changes in all projects
$ clowder clean

# Discard changes in projects in clang group
$ clowder clean -g clang

# Discard changes in clang project
$ clowder clean -p llvm-mirror/clang
```

---

## `clowder diff`

Equivalent to running `git status -vv` in project directories

```bash
# Print git diff status for all projects
$ clowder diff

# Print git diff status for projects in clang group
$ clowder diff -g clang

# Print git diff status for clang project
$ clowder diff -p llvm-mirror/clang
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

# Run command for projects in clang group
$ clowder forall -c "git status" -g clang

# Run script for projects in clang group
$ clowder forall -c "/path/to/script.sh" -g clang

# Run command for clang project
$ clowder forall -c "git status" -p llvm-mirror/clang

# Run script for clang project
$ clowder forall -c "/path/to/script.sh" -p llvm-mirror/clang
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

# Only herd projects in clang and llvm groups
$ clowder herd -g clang llvm

# Only herd clang project
$ clowder herd -p llvm-mirror/clang
```

---

## `clowder init`

Clone repo containing `clowder.yaml` file (referred to as the "clowder repo")

```bash
# Clone clowder repo
$ clowder init https://github.com/jrgoodle/llvm-projects.git

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

# Prune branch 'stale_branch' in clang group
$ clowder prune stale_branch -g clang

# Prune branch 'stale_branch' in clang project
$ clowder prune stale_branch -p llvm-mirror/clang
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

# Create new local branch 'my_feature' in clang group
$ clowder start my_feature -g clang

# Create new local branch 'my_feature' in clang project
$ clowder start my_feature -p llvm-mirror/clang
```

---

## `clowder stash`

Stash changes in dirty repositories

```bash
# Stash any changes in projects
$ clowder stash

# Stash any changes in projects in clang group
$ clowder stash -g clang

# Stash any changes in clang project
$ clowder stash -p llvm-mirror/clang
```

---

## `clowder status`

Print status of projects

```bash
# Print status of projects
$ clowder status

# Fetch upstream changes for projects before printing statuses
$ clowder status -f
```
