## `clowder` Commands

- [clowder clean](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#clean)
- [clowder forall](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#forall)
- [clowder herd](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#herd)
- [clowder init](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#init)
- [clowder link](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#link)
- [clowder repo](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#repo)
- [clowder save](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#save)
- [clowder start](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#start)
- [clowder stash](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#stash)
- [clowder status](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#status)
- [clowder prune](https://github.com/JrGoodle/clowder/blob/master/docs/commands.md#prune)

---

### `clean`

Discards changes in dirty repositories.

```bash
# Discard changes in all projects
$ clowder clean

# Discard changes in projects in clang group
$ clowder clean -g clang

# Discard changes in clang project
$ clowder clean -p llvm-mirror/clang
```

---

### `forall`

Runs command in project directories.

```bash
# Run command in all project directories
$ clowder forall -c "git status"

# Run script in all project directories
$ clowder forall -f "/path/to/script.sh"

# Run command in all project directories, ignoring errors
$ clowder forall -ic "git status"

# Run script in all project directories, ignoring errors
$ clowder forall -if "/path/to/script.sh"

# Run command for projects in clang group
$ clowder forall -c "git status" -g clang

# Run script for projects in clang group
$ clowder forall -f "/path/to/script.sh" -g clang

# Run command for clang project
$ clowder forall -c "git status" -p llvm-mirror/clang

# Run script for clang project
$ clowder forall -f "/path/to/script.sh" -p llvm-mirror/clang
```

---

### `herd`

Update with latest changes.

```bash
# Herd a shallow clone to specified depth
$ clowder herd -d 1

# Only herd projects in clang and llvm groups
$ clowder herd -g clang llvm

# Only herd clang project
$ clowder herd -p llvm-mirror/clang
```

---

### `init`

Clone repo containing `clowder.yaml` file ('clowder repo').

```bash
# Clone clowder repo
$ clowder init https://github.com/jrgoodle/llvm-projects.git

# Clone clowder repo from branch 'tags'
$ clowder init https://github.com/jrgoodle/cats.git -b tags
```

---

### `link`

Set `clowder.yaml` symlink.

```bash
# Point clowder.yaml symlink to default clowder.yaml file
$ clowder link

# Point clowder.yaml symlink to saved version
$ clowder link -v 0.1
```

---

### `prune`

Prune stale local branches.

```bash
# Prune branch 'stale_branch' for all projects
$ clowder prune stale_branch

# Force prune branch 'stale_branch' for all projects
$ clowder prune -f stale_branch

# Prune remote branch 'stale_branch' for all projects
$ clowder prune -r stale_branch

# Prune branch 'stale_branch' in clang group
$ clowder prune stale_branch -g clang

# Prune branch 'stale_branch' in clang project
$ clowder prune stale_branch -p llvm-mirror/clang
```

---

### `repo`

Convenience commands for managing clowder repo (the `.clowder` directory).
More advanced needs may require changing to the `.clowder` directory and running commands directly.

```bash
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

### `save`

Save a `clowder.yaml` version with the information from currently checked out repositories.
Versions are saved to `.clowder/versions/<version_name>/clowder.yaml`.

```bash
# Save a version of clowder.yaml with current commit sha's
$ clowder save 0.1
```

---

### `start`

Start a new feature branch or check out if it already exists.

```bash
# Create new branch 'my_feature' for all projects
$ clowder start my_feature

# Create new branch 'my_feature' in clang group
$ clowder start my_feature -g clang

# Create new branch 'my_feature' in clang project
$ clowder start my_feature -p llvm-mirror/clang
```

---

### `stash`

Stash changes in dirty repositories.

```bash
# Stash any changes in projects
$ clowder stash

# Stash any changes in projects in clang group
$ clowder stash -g clang

# Stash any changes in clang project
$ clowder stash -p llvm-mirror/clang
```

---

### `status`

Print status of projects.

```bash
# Print status of projects
$ clowder status

# Print more verbose status of projects
$ clowder status -v

# Fetch upstream changes for projects before printing statuses
$ clowder status -f

# Print status of projects in clang and llvm groups
$ clowder status -g clang llvm

# Print status of clang and llvm projects
$ clowder status -p llvm-mirror/clang llvm-mirror/llvm

# Print verbose status of projects in clang group
$ clowder status -v -g clang

# Print verbose status of clang and llvm projects
$ clowder status -v -p llvm-mirror/clang llvm-mirror/llvm
```
